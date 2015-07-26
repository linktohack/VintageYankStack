from pprint import pprint

import sublime, sublime_plugin
from Vintage.vintage import g_registers, clip_empty_selection_to_line_contents

debug = lambda *args, **kwargs: None
debug = print

def last_command_before_yank_stack(view):
    i = 0;
    while True:
        last_command = view.command_history(i)
        if last_command[0] != 'vi_yank_stack':
            break
        else:
            i = i - 1
    return last_command

class InputStateTracker(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if key == "vi_has_just_pasted":
            last_command = last_command_before_yank_stack(view)
            has_just_pasted = last_command[0] in ('vi_paste_left', 'vi_paste_right')
            # debug('last_command', last_command)
            # debug('has_just_pasted', has_just_pasted)
            if operator == sublime.OP_EQUAL:
                return operand == has_just_pasted
            if operator == sublime.OP_NOT_EQUAL:
                return operand != has_just_pasted
        return None

class ViYankStackCommand(sublime_plugin.TextCommand):
    def run_(self, edit_token, args):
        if 'event' in args:
            del args['event']

        return self.run(**args)

    def run(self, forward=False, fallback_command=False,
            fallback_scope = 'window', fallback_args = {}):
        debug('current g_registers')
        pprint(g_registers)
        last_command = last_command_before_yank_stack(self.view)
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

                del g_registers['_']
                g_registers['"'] = g_registers['0']
                debug('shifted g_registers')
                pprint(g_registers)
                if self.view.settings().get('vintage_use_clipboard', False):
                    sublime.set_clipboard(g_registers['0'])
                    g_registers['+'] = g_registers['0']
                    g_registers['*'] = g_registers['0']
            except KeyError:
                pass
            else:
                debug('undo')
                self.view.window().run_command('undo')
                debug('last_command', last_command)
                for _ in range(last_command[2]):
                    self.view.run_command(*last_command[:2])

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
    else:
        if register == '0':
            for i in range(9, 0, -1):
                if '%s' % (i - 1) in g_registers:
                    g_registers['%s' % i] = g_registers['%s' % (i - 1)]
        reg = register.lower()
        append = (reg != register)

        if append and reg in g_registers:
            g_registers[reg] += text
        else:
            g_registers[reg] = text
    debug('g_registers')
    pprint(g_registers)