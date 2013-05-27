import sublime, sublime_plugin
from vintage import g_registers

def run_fallback_command(window, command, scope, args):
    if command:
        if scope == 'window':
            window.run_command(command, args)
        elif scope == 'view':
            window.active_view().run_command(command, args)
        else:
            print 'ViYankStack: fallback command scope undefined!'

class ViYankStackCommand(sublime_plugin.WindowCommand):
    def run(self, forward = False, fallback_command = False,
            fallback_scope = 'window', fallback_args = {}):
        last_command = self.window.active_view().command_history(0)
        if last_command[0] in ('vi_paste_left', 'vi_paste_right'):
            for i in xrange(9, -1, -1):
                    if '%s' % i in g_registers:
                        top = i
                        break
            try:
                if not forward:
                    g_registers['_'] = g_registers['0']
                    for i in xrange(0, top):
                        g_registers['%s' % i] = g_registers['%s' % (i + 1)]
                    g_registers['%s' % top] = g_registers['_']
                else:
                    g_registers['_'] = g_registers['%s' % top]
                    for i in xrange(top, 0, -1):
                        g_registers['%s' % i] = g_registers['%s' % (i - 1)]
                    g_registers['0'] = g_registers['_']

                g_registers['"'] = g_registers['0']
                g_registers['+'] = g_registers['0']
                g_registers['*'] = g_registers['0']
                sublime.set_clipboard(g_registers['0'])
            except KeyError:
                pass
            else:
                self.window.run_command('undo')
                self.window.active_view().run_command(last_command[0],
                                                  last_command[1])
        elif fallback_command:
            run_fallback_command(self.window, fallback_command,
                                fallback_scope, fallback_args)
