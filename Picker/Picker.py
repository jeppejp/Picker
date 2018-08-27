import curses

BLACK_ON_WHITE = 10
RED = 1
GREEN = 2
YELLOW = 4
BLUE = 3
MAGENTA = 0
CYAN = 0
WHITE = 0
NOCOL = 0


class Picker:
    def __init__(self, config):
        self._result = ''
        self._categories = []
        self._config = config

    def pick(self):
        curses.wrapper(self._main)
        return self._result

    def add_category(self, name, lst):
        self._categories.append({'name': name, 'lst': lst})

    def add_to_category(self, category, entry):
        for c in self._categories:
            if c['name'] == category:
                c['lst'].append(entry)
                return True
        return False

    def _has_match(self, haystack, needles):
        if not needles:
            return True
        for n in needles.split():
            if n.lower() not in haystack.lower():
                return False
        return True

    def _main(self, stdscr):
        stdscr.timeout(100)
        curses.start_color()
        curses.use_default_colors()

        query = ''

        curses.init_pair(0, curses.COLOR_WHITE, -1)
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_BLUE, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)

        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.curs_set(False)

        idx = 0
        cat_idx = 0
        s = 1
        cat_names = []

        for c in self._categories:
            cat_names.append(c['name'])

        while True:
            matches = []
            (maxy, maxx) = stdscr.getmaxyx()
            for t in self._categories[cat_idx]['lst']:
                if self._has_match(t[0], query):
                    matches.append(t)
            stdscr.refresh()
            offset = 0
            for i, c in enumerate(cat_names):
                if i == cat_idx:
                    stdscr.addstr(0, offset, c, curses.color_pair(10))
                else:
                    stdscr.addstr(0, offset, c)
                offset += len(c) + 4

            for i in range(0, maxy - 4):
                if i < len(matches):
                    t = matches[i]
                    if i == idx:
                        stdscr.addstr(i + 3, 0, '> %-100s' % t[0], curses.color_pair(t[1]))
                    else:
                        stdscr.addstr(i + 3, 0, '  %-100s' % t[0], curses.color_pair(t[1]))
                else:
                    stdscr.addstr(i + 3, 0, ' ' * maxx)

            # stdscr.addstr(2, 0, str(s))  # DEBUG
            stdscr.addstr(1, 0, "SEARCH: %-100s" % query)
            try:
                s = stdscr.getch()
            except KeyboardInterrupt:
                return
            if s == 27:  # ESC
                return
            elif s == curses.KEY_BACKSPACE:  # Backspace
                query = query[:-1]
            elif s == 10:
                self._result = matches[idx]
                return
            elif s == curses.KEY_DOWN or (self._config.get('hjkl', True) and s == ord('J')):
                idx += 1
                idx = min(idx, len(matches) - 1)
            elif s == curses.KEY_UP or (self._config.get('hjkl', True) and s == ord('K')):
                idx -= 1
                idx = max(idx, 0)
            elif s == curses.KEY_RIGHT or (self._config.get('hjkl', True) and s == ord('L')):
                cat_idx += 1
                cat_idx = min(cat_idx, len(cat_names) - 1)
                query = ''
                idx = 0
            elif s == curses.KEY_LEFT or (self._config.get('hjkl', True) and s == ord('H')):
                cat_idx -= 1
                cat_idx = max(cat_idx, 0)
                query = ''
                idx = 0
            elif s < 256:  # perhaps a valid char...
                try:
                    query += chr(s)
                    idx = 0
                except ValueError:
                    pass
