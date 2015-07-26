import sublime, sublime_plugin
from Vintage.vintage import g_registers, clip_empty_selection_to_line_contents

def run_fallback_command(view, command, scope, args):
    if command:
        if scope == 'window':
            view.window().run_command(command, args)
        elif scope == 'view':
            view.run_command(command, args)
        else:
            raise Exception('ViYankStack: fallback command scope undefined!')

class ViYankStackCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward=False, fallback_command=False,
            fallback_scope = 'window', fallback_args = {}):
        last_command = self.view.command_history(0)
        if last_command[0] in ('vi_paste_left', 'vi_paste_right'):
            for i in range(9, -1, -1):
                    if '%s' % i in g_registers:
                        top = i
                        break
            try:
                if not forward:
                    g_registers['_'] = g_registers['0']
                    for i in range(0, top):
                        g_registers['%s' % i] = g_registers['%s' % (i + 1)]
                    g_registers['%s' % top] = g_registers['_']
                else:
                    g_registers['_'] = g_registers['%s' % top]
                    for i in range(top, 0, -1):
                        g_registers['%s' % i] = g_registers['%s' % (i - 1)]
                    g_registers['0'] = g_registers['_']

                g_registers['"'] = g_registers['0']
                g_registers['+'] = g_registers['0']
                g_registers['*'] = g_registers['0']
                
                if self.view.settings().get('vintage_use_clipboard', False):
                    sublime.set_clipboard(g_registers['0'])
            except KeyError:
                pass
            else:
                self.view.window().run_command('undo')
                self.view.run_command(last_command[0], last_command[1])
        elif fallback_command:
            run_fallback_command(self.view, fallback_command,
                                 fallback_scope, fallback_args)

# Override ViDelete series
class ViDelete(sublime_plugin.TextCommand):
    def run(self, edit, register = '"'):
        if self.view.has_non_empty_selection_region():
            set_register(self.view, register, forward=False)
            set_register(self.view, '0', forward=False)
            self.view.run_command('left_delete')

class ViLeftDelete(sublime_plugin.TextCommand):
    def run(self, edit, register = '"'):
        set_register(self.view, register, forward=False)
        set_register(self.view, '0', forward=False)
        self.view.run_command('left_delete')
        clip_empty_selection_to_line_contents(self.view)

class ViRightDelete(sublime_plugin.TextCommand):
    def run(self, edit, register = '"'):
        set_register(self.view, register, forward=True)
        set_register(self.view, '0', forward=True)
        self.view.run_command('right_delete')
        clip_empty_selection_to_line_contents(self.view)

def set_register(view, register, forward):
    delta = 1
    if not forward:
        delta = -1

    text = []
    regions = []
    for s in view.sel():
        if s.empty():
            s = sublime.Region(s.a, s.a + delta)
        text.append(view.substr(s))
        regions.append(s)

    text = '\n'.join(text)

    use_sys_clipboard = view.settings().get('vintage_use_clipboard', False) == True

    if (use_sys_clipboard and register == '"') or (register in ('*', '+')):
        sublime.set_clipboard(text)
        # If the system's clipboard is used, Vim always propagates the data to
        # the unnamed register too.
        register = '"'

    if register == '%':
        pass
    elif register == '0':
        for i in range(9, 0, -1):
            if '%s' % (i - 1) in g_registers:
                g_registers['%s' % i] = g_registers['%s' % (i - 1)]
    else:
        reg = register.lower()
        append = (reg != register)

        if append and reg in g_registers:
            g_registers[reg] += text
        else:
            g_registers[reg] = text
