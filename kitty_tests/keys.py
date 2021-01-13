#!/usr/bin/env python3
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from functools import partial
import kitty.fast_data_types as defines
from . import BaseTest


class TestKeys(BaseTest):

    def test_encode_key_event(self):
        enc = defines.encode_key_for_tty
        ae = self.assertEqual
        shift, alt, ctrl, super = defines.GLFW_MOD_SHIFT, defines.GLFW_MOD_ALT, defines.GLFW_MOD_CONTROL, defines.GLFW_MOD_SUPER  # noqa
        press, repeat, release = defines.GLFW_PRESS, defines.GLFW_REPEAT, defines.GLFW_RELEASE  # noqa

        def csi(mods=0, num=1, trailer='u'):
            ans = '\033['
            if num != 1 or mods:
                ans += f'{num}'
            if mods:
                m = 0
                if mods & shift:
                    m |= 1
                if mods & alt:
                    m |= 2
                if mods & ctrl:
                    m |= 4
                if mods & super:
                    m |= 8
                ans += f';{m+1}'
            return ans + trailer

        def mods_test(key, plain=None, shift=None, ctrl=None, alt=None, calt=None, cshift=None, ashift=None, csi_num=None, trailer='u'):
            c = partial(csi, num=csi_num or key, trailer=trailer)
            e = partial(enc, key=key)

            def a(a, b):
                ae(a, b, f"{a.encode('ascii')} != {b.encode('ascii')}")
            a(e(), plain or c())
            a(e(mods=defines.GLFW_MOD_SHIFT), shift or c(defines.GLFW_MOD_SHIFT))
            a(e(mods=defines.GLFW_MOD_CONTROL), ctrl or c(defines.GLFW_MOD_CONTROL))
            a(e(mods=defines.GLFW_MOD_ALT | defines.GLFW_MOD_CONTROL), calt or c(defines.GLFW_MOD_ALT | defines.GLFW_MOD_CONTROL))
            a(e(mods=defines.GLFW_MOD_SHIFT | defines.GLFW_MOD_CONTROL), cshift or c(defines.GLFW_MOD_CONTROL | defines.GLFW_MOD_SHIFT))
            a(e(mods=defines.GLFW_MOD_SHIFT | defines.GLFW_MOD_ALT), ashift or c(defines.GLFW_MOD_ALT | defines.GLFW_MOD_SHIFT))

        mods_test(defines.GLFW_FKEY_ENTER, '\x0d', alt='\033\x0d', csi_num=ord('\r'))
        mods_test(defines.GLFW_FKEY_KP_ENTER, '\x0d', alt='\033\x0d', csi_num=ord('\r'))
        mods_test(defines.GLFW_FKEY_ESCAPE, '\x1b', alt='\033\033', csi_num=27)
        mods_test(defines.GLFW_FKEY_BACKSPACE, '\x7f', alt='\033\x7f', ctrl='\x08', csi_num=127)
        mods_test(defines.GLFW_FKEY_TAB, '\t', alt='\033\t', shift='\x1b[Z', csi_num=ord('\t'))
        mods_test(defines.GLFW_FKEY_INSERT, csi_num=2, trailer='~')
        mods_test(defines.GLFW_FKEY_KP_INSERT, csi_num=2, trailer='~')
        mods_test(defines.GLFW_FKEY_DELETE, csi_num=3, trailer='~')
        mods_test(defines.GLFW_FKEY_KP_DELETE, csi_num=3, trailer='~')
        mods_test(defines.GLFW_FKEY_PAGE_UP, csi_num=5, trailer='~')
        mods_test(defines.GLFW_FKEY_KP_PAGE_UP, csi_num=5, trailer='~')
        mods_test(defines.GLFW_FKEY_KP_PAGE_DOWN, csi_num=6, trailer='~')
        mods_test(defines.GLFW_FKEY_HOME, csi_num=1, trailer='H')
        mods_test(defines.GLFW_FKEY_KP_HOME, csi_num=1, trailer='H')
        mods_test(defines.GLFW_FKEY_END, csi_num=1, trailer='F')
        mods_test(defines.GLFW_FKEY_KP_END, csi_num=1, trailer='F')
        mods_test(defines.GLFW_FKEY_F1, csi_num=1, trailer='P')
        mods_test(defines.GLFW_FKEY_F2, csi_num=1, trailer='Q')
        mods_test(defines.GLFW_FKEY_F3, csi_num=1, trailer='R')
        mods_test(defines.GLFW_FKEY_F4, csi_num=1, trailer='S')
        mods_test(defines.GLFW_FKEY_F5, csi_num=15, trailer='~')
        mods_test(defines.GLFW_FKEY_F6, csi_num=17, trailer='~')
        mods_test(defines.GLFW_FKEY_F7, csi_num=18, trailer='~')
        mods_test(defines.GLFW_FKEY_F8, csi_num=19, trailer='~')
        mods_test(defines.GLFW_FKEY_F9, csi_num=20, trailer='~')
        mods_test(defines.GLFW_FKEY_F10, csi_num=21, trailer='~')
        mods_test(defines.GLFW_FKEY_F11, csi_num=23, trailer='~')
        mods_test(defines.GLFW_FKEY_F12, csi_num=24, trailer='~')
        mods_test(defines.GLFW_FKEY_UP, csi_num=1, trailer='A')
        mods_test(defines.GLFW_FKEY_KP_UP, csi_num=1, trailer='A')
        mods_test(defines.GLFW_FKEY_DOWN, csi_num=1, trailer='B')
        mods_test(defines.GLFW_FKEY_KP_DOWN, csi_num=1, trailer='B')
        mods_test(defines.GLFW_FKEY_RIGHT, csi_num=1, trailer='C')
        mods_test(defines.GLFW_FKEY_KP_RIGHT, csi_num=1, trailer='C')
        mods_test(defines.GLFW_FKEY_LEFT, csi_num=1, trailer='D')
        mods_test(defines.GLFW_FKEY_KP_LEFT, csi_num=1, trailer='D')

        # legacy key tests {{{
        # start legacy letter tests (auto generated by gen-key-constants.py do not edit)
        ae(enc(ord('`')), '`')
        ae(enc(ord('`'), mods=shift), '~')
        ae(enc(ord('`'), mods=alt), "\x1b" + '`')
        ae(enc(ord('`'), mods=shift | alt), "\x1b" + '~')
        ae(enc(ord('`'), mods=ctrl), ' ')
        ae(enc(ord('`'), mods=ctrl | alt), "\x1b" + ' ')
        ae(enc(ord('1')), '1')
        ae(enc(ord('1'), mods=shift), '!')
        ae(enc(ord('1'), mods=alt), "\x1b" + '1')
        ae(enc(ord('1'), mods=shift | alt), "\x1b" + '!')
        ae(enc(ord('1'), mods=ctrl), '1')
        ae(enc(ord('1'), mods=ctrl | alt), "\x1b" + '1')
        ae(enc(ord('2')), '2')
        ae(enc(ord('2'), mods=shift), '@')
        ae(enc(ord('2'), mods=alt), "\x1b" + '2')
        ae(enc(ord('2'), mods=shift | alt), "\x1b" + '@')
        ae(enc(ord('2'), mods=ctrl), '2')
        ae(enc(ord('2'), mods=ctrl | alt), "\x1b" + '2')
        ae(enc(ord('3')), '3')
        ae(enc(ord('3'), mods=shift), '#')
        ae(enc(ord('3'), mods=alt), "\x1b" + '3')
        ae(enc(ord('3'), mods=shift | alt), "\x1b" + '#')
        ae(enc(ord('3'), mods=ctrl), '3')
        ae(enc(ord('3'), mods=ctrl | alt), "\x1b" + '3')
        ae(enc(ord('4')), '4')
        ae(enc(ord('4'), mods=shift), '$')
        ae(enc(ord('4'), mods=alt), "\x1b" + '4')
        ae(enc(ord('4'), mods=shift | alt), "\x1b" + '$')
        ae(enc(ord('4'), mods=ctrl), '4')
        ae(enc(ord('4'), mods=ctrl | alt), "\x1b" + '4')
        ae(enc(ord('5')), '5')
        ae(enc(ord('5'), mods=shift), '%')
        ae(enc(ord('5'), mods=alt), "\x1b" + '5')
        ae(enc(ord('5'), mods=shift | alt), "\x1b" + '%')
        ae(enc(ord('5'), mods=ctrl), '5')
        ae(enc(ord('5'), mods=ctrl | alt), "\x1b" + '5')
        ae(enc(ord('6')), '6')
        ae(enc(ord('6'), mods=shift), '^')
        ae(enc(ord('6'), mods=alt), "\x1b" + '6')
        ae(enc(ord('6'), mods=shift | alt), "\x1b" + '^')
        ae(enc(ord('6'), mods=ctrl), '6')
        ae(enc(ord('6'), mods=ctrl | alt), "\x1b" + '6')
        ae(enc(ord('7')), '7')
        ae(enc(ord('7'), mods=shift), '&')
        ae(enc(ord('7'), mods=alt), "\x1b" + '7')
        ae(enc(ord('7'), mods=shift | alt), "\x1b" + '&')
        ae(enc(ord('7'), mods=ctrl), '7')
        ae(enc(ord('7'), mods=ctrl | alt), "\x1b" + '7')
        ae(enc(ord('8')), '8')
        ae(enc(ord('8'), mods=shift), '*')
        ae(enc(ord('8'), mods=alt), "\x1b" + '8')
        ae(enc(ord('8'), mods=shift | alt), "\x1b" + '*')
        ae(enc(ord('8'), mods=ctrl), '8')
        ae(enc(ord('8'), mods=ctrl | alt), "\x1b" + '8')
        ae(enc(ord('9')), '9')
        ae(enc(ord('9'), mods=shift), '(')
        ae(enc(ord('9'), mods=alt), "\x1b" + '9')
        ae(enc(ord('9'), mods=shift | alt), "\x1b" + '(')
        ae(enc(ord('9'), mods=ctrl), '9')
        ae(enc(ord('9'), mods=ctrl | alt), "\x1b" + '9')
        ae(enc(ord('0')), '0')
        ae(enc(ord('0'), mods=shift), ')')
        ae(enc(ord('0'), mods=alt), "\x1b" + '0')
        ae(enc(ord('0'), mods=shift | alt), "\x1b" + ')')
        ae(enc(ord('0'), mods=ctrl), '0')
        ae(enc(ord('0'), mods=ctrl | alt), "\x1b" + '0')
        ae(enc(ord('-')), '-')
        ae(enc(ord('-'), mods=shift), '_')
        ae(enc(ord('-'), mods=alt), "\x1b" + '-')
        ae(enc(ord('-'), mods=shift | alt), "\x1b" + '_')
        ae(enc(ord('-'), mods=ctrl), '-')
        ae(enc(ord('-'), mods=ctrl | alt), "\x1b" + '-')
        ae(enc(ord('=')), '=')
        ae(enc(ord('='), mods=shift), '+')
        ae(enc(ord('='), mods=alt), "\x1b" + '=')
        ae(enc(ord('='), mods=shift | alt), "\x1b" + '+')
        ae(enc(ord('='), mods=ctrl), '=')
        ae(enc(ord('='), mods=ctrl | alt), "\x1b" + '=')
        ae(enc(ord('[')), '[')
        ae(enc(ord('['), mods=shift), '{')
        ae(enc(ord('['), mods=alt), "\x1b" + '[')
        ae(enc(ord('['), mods=shift | alt), "\x1b" + '{')
        ae(enc(ord('['), mods=ctrl), '\x1b')
        ae(enc(ord('['), mods=ctrl | alt), "\x1b" + '\x1b')
        ae(enc(ord(']')), ']')
        ae(enc(ord(']'), mods=shift), '}')
        ae(enc(ord(']'), mods=alt), "\x1b" + ']')
        ae(enc(ord(']'), mods=shift | alt), "\x1b" + '}')
        ae(enc(ord(']'), mods=ctrl), '\x1d')
        ae(enc(ord(']'), mods=ctrl | alt), "\x1b" + '\x1d')
        ae(enc(ord('\\')), '\\')
        ae(enc(ord('\\'), mods=shift), '|')
        ae(enc(ord('\\'), mods=alt), "\x1b" + '\\')
        ae(enc(ord('\\'), mods=shift | alt), "\x1b" + '|')
        ae(enc(ord('\\'), mods=ctrl), '\x1c')
        ae(enc(ord('\\'), mods=ctrl | alt), "\x1b" + '\x1c')
        ae(enc(ord(';')), ';')
        ae(enc(ord(';'), mods=shift), ':')
        ae(enc(ord(';'), mods=alt), "\x1b" + ';')
        ae(enc(ord(';'), mods=shift | alt), "\x1b" + ':')
        ae(enc(ord(';'), mods=ctrl), ';')
        ae(enc(ord(';'), mods=ctrl | alt), "\x1b" + ';')
        ae(enc(ord("'")), "'")
        ae(enc(ord("'"), mods=shift), '"')
        ae(enc(ord("'"), mods=alt), "\x1b" + "'")
        ae(enc(ord("'"), mods=shift | alt), "\x1b" + '"')
        ae(enc(ord("'"), mods=ctrl), "'")
        ae(enc(ord("'"), mods=ctrl | alt), "\x1b" + "'")
        ae(enc(ord(',')), ',')
        ae(enc(ord(','), mods=shift), '<')
        ae(enc(ord(','), mods=alt), "\x1b" + ',')
        ae(enc(ord(','), mods=shift | alt), "\x1b" + '<')
        ae(enc(ord(','), mods=ctrl), ',')
        ae(enc(ord(','), mods=ctrl | alt), "\x1b" + ',')
        ae(enc(ord('.')), '.')
        ae(enc(ord('.'), mods=shift), '>')
        ae(enc(ord('.'), mods=alt), "\x1b" + '.')
        ae(enc(ord('.'), mods=shift | alt), "\x1b" + '>')
        ae(enc(ord('.'), mods=ctrl), '.')
        ae(enc(ord('.'), mods=ctrl | alt), "\x1b" + '.')
        ae(enc(ord('/')), '/')
        ae(enc(ord('/'), mods=shift), '?')
        ae(enc(ord('/'), mods=alt), "\x1b" + '/')
        ae(enc(ord('/'), mods=shift | alt), "\x1b" + '?')
        ae(enc(ord('/'), mods=ctrl), '/')
        ae(enc(ord('/'), mods=ctrl | alt), "\x1b" + '/')
        ae(enc(ord('a')), 'a')
        ae(enc(ord('a'), mods=shift), 'A')
        ae(enc(ord('a'), mods=alt), "\x1b" + 'a')
        ae(enc(ord('a'), mods=shift | alt), "\x1b" + 'A')
        ae(enc(ord('a'), mods=ctrl), '!')
        ae(enc(ord('a'), mods=ctrl | alt), "\x1b" + '!')
        ae(enc(ord('b')), 'b')
        ae(enc(ord('b'), mods=shift), 'B')
        ae(enc(ord('b'), mods=alt), "\x1b" + 'b')
        ae(enc(ord('b'), mods=shift | alt), "\x1b" + 'B')
        ae(enc(ord('b'), mods=ctrl), '"')
        ae(enc(ord('b'), mods=ctrl | alt), "\x1b" + '"')
        ae(enc(ord('c')), 'c')
        ae(enc(ord('c'), mods=shift), 'C')
        ae(enc(ord('c'), mods=alt), "\x1b" + 'c')
        ae(enc(ord('c'), mods=shift | alt), "\x1b" + 'C')
        ae(enc(ord('c'), mods=ctrl), '#')
        ae(enc(ord('c'), mods=ctrl | alt), "\x1b" + '#')
        ae(enc(ord('d')), 'd')
        ae(enc(ord('d'), mods=shift), 'D')
        ae(enc(ord('d'), mods=alt), "\x1b" + 'd')
        ae(enc(ord('d'), mods=shift | alt), "\x1b" + 'D')
        ae(enc(ord('d'), mods=ctrl), '$')
        ae(enc(ord('d'), mods=ctrl | alt), "\x1b" + '$')
        ae(enc(ord('e')), 'e')
        ae(enc(ord('e'), mods=shift), 'E')
        ae(enc(ord('e'), mods=alt), "\x1b" + 'e')
        ae(enc(ord('e'), mods=shift | alt), "\x1b" + 'E')
        ae(enc(ord('e'), mods=ctrl), '%')
        ae(enc(ord('e'), mods=ctrl | alt), "\x1b" + '%')
        ae(enc(ord('f')), 'f')
        ae(enc(ord('f'), mods=shift), 'F')
        ae(enc(ord('f'), mods=alt), "\x1b" + 'f')
        ae(enc(ord('f'), mods=shift | alt), "\x1b" + 'F')
        ae(enc(ord('f'), mods=ctrl), '&')
        ae(enc(ord('f'), mods=ctrl | alt), "\x1b" + '&')
        ae(enc(ord('g')), 'g')
        ae(enc(ord('g'), mods=shift), 'G')
        ae(enc(ord('g'), mods=alt), "\x1b" + 'g')
        ae(enc(ord('g'), mods=shift | alt), "\x1b" + 'G')
        ae(enc(ord('g'), mods=ctrl), "'")
        ae(enc(ord('g'), mods=ctrl | alt), "\x1b" + "'")
        ae(enc(ord('h')), 'h')
        ae(enc(ord('h'), mods=shift), 'H')
        ae(enc(ord('h'), mods=alt), "\x1b" + 'h')
        ae(enc(ord('h'), mods=shift | alt), "\x1b" + 'H')
        ae(enc(ord('h'), mods=ctrl), '(')
        ae(enc(ord('h'), mods=ctrl | alt), "\x1b" + '(')
        ae(enc(ord('i')), 'i')
        ae(enc(ord('i'), mods=shift), 'I')
        ae(enc(ord('i'), mods=alt), "\x1b" + 'i')
        ae(enc(ord('i'), mods=shift | alt), "\x1b" + 'I')
        ae(enc(ord('i'), mods=ctrl), ')')
        ae(enc(ord('i'), mods=ctrl | alt), "\x1b" + ')')
        ae(enc(ord('j')), 'j')
        ae(enc(ord('j'), mods=shift), 'J')
        ae(enc(ord('j'), mods=alt), "\x1b" + 'j')
        ae(enc(ord('j'), mods=shift | alt), "\x1b" + 'J')
        ae(enc(ord('j'), mods=ctrl), '*')
        ae(enc(ord('j'), mods=ctrl | alt), "\x1b" + '*')
        ae(enc(ord('k')), 'k')
        ae(enc(ord('k'), mods=shift), 'K')
        ae(enc(ord('k'), mods=alt), "\x1b" + 'k')
        ae(enc(ord('k'), mods=shift | alt), "\x1b" + 'K')
        ae(enc(ord('k'), mods=ctrl), '+')
        ae(enc(ord('k'), mods=ctrl | alt), "\x1b" + '+')
        ae(enc(ord('l')), 'l')
        ae(enc(ord('l'), mods=shift), 'L')
        ae(enc(ord('l'), mods=alt), "\x1b" + 'l')
        ae(enc(ord('l'), mods=shift | alt), "\x1b" + 'L')
        ae(enc(ord('l'), mods=ctrl), ',')
        ae(enc(ord('l'), mods=ctrl | alt), "\x1b" + ',')
        ae(enc(ord('m')), 'm')
        ae(enc(ord('m'), mods=shift), 'M')
        ae(enc(ord('m'), mods=alt), "\x1b" + 'm')
        ae(enc(ord('m'), mods=shift | alt), "\x1b" + 'M')
        ae(enc(ord('m'), mods=ctrl), '-')
        ae(enc(ord('m'), mods=ctrl | alt), "\x1b" + '-')
        ae(enc(ord('n')), 'n')
        ae(enc(ord('n'), mods=shift), 'N')
        ae(enc(ord('n'), mods=alt), "\x1b" + 'n')
        ae(enc(ord('n'), mods=shift | alt), "\x1b" + 'N')
        ae(enc(ord('n'), mods=ctrl), '.')
        ae(enc(ord('n'), mods=ctrl | alt), "\x1b" + '.')
        ae(enc(ord('o')), 'o')
        ae(enc(ord('o'), mods=shift), 'O')
        ae(enc(ord('o'), mods=alt), "\x1b" + 'o')
        ae(enc(ord('o'), mods=shift | alt), "\x1b" + 'O')
        ae(enc(ord('o'), mods=ctrl), '/')
        ae(enc(ord('o'), mods=ctrl | alt), "\x1b" + '/')
        ae(enc(ord('p')), 'p')
        ae(enc(ord('p'), mods=shift), 'P')
        ae(enc(ord('p'), mods=alt), "\x1b" + 'p')
        ae(enc(ord('p'), mods=shift | alt), "\x1b" + 'P')
        ae(enc(ord('p'), mods=ctrl), '0')
        ae(enc(ord('p'), mods=ctrl | alt), "\x1b" + '0')
        ae(enc(ord('q')), 'q')
        ae(enc(ord('q'), mods=shift), 'Q')
        ae(enc(ord('q'), mods=alt), "\x1b" + 'q')
        ae(enc(ord('q'), mods=shift | alt), "\x1b" + 'Q')
        ae(enc(ord('q'), mods=ctrl), '1')
        ae(enc(ord('q'), mods=ctrl | alt), "\x1b" + '1')
        ae(enc(ord('r')), 'r')
        ae(enc(ord('r'), mods=shift), 'R')
        ae(enc(ord('r'), mods=alt), "\x1b" + 'r')
        ae(enc(ord('r'), mods=shift | alt), "\x1b" + 'R')
        ae(enc(ord('r'), mods=ctrl), '2')
        ae(enc(ord('r'), mods=ctrl | alt), "\x1b" + '2')
        ae(enc(ord('s')), 's')
        ae(enc(ord('s'), mods=shift), 'S')
        ae(enc(ord('s'), mods=alt), "\x1b" + 's')
        ae(enc(ord('s'), mods=shift | alt), "\x1b" + 'S')
        ae(enc(ord('s'), mods=ctrl), '3')
        ae(enc(ord('s'), mods=ctrl | alt), "\x1b" + '3')
        ae(enc(ord('t')), 't')
        ae(enc(ord('t'), mods=shift), 'T')
        ae(enc(ord('t'), mods=alt), "\x1b" + 't')
        ae(enc(ord('t'), mods=shift | alt), "\x1b" + 'T')
        ae(enc(ord('t'), mods=ctrl), '4')
        ae(enc(ord('t'), mods=ctrl | alt), "\x1b" + '4')
        ae(enc(ord('u')), 'u')
        ae(enc(ord('u'), mods=shift), 'U')
        ae(enc(ord('u'), mods=alt), "\x1b" + 'u')
        ae(enc(ord('u'), mods=shift | alt), "\x1b" + 'U')
        ae(enc(ord('u'), mods=ctrl), '5')
        ae(enc(ord('u'), mods=ctrl | alt), "\x1b" + '5')
        ae(enc(ord('v')), 'v')
        ae(enc(ord('v'), mods=shift), 'V')
        ae(enc(ord('v'), mods=alt), "\x1b" + 'v')
        ae(enc(ord('v'), mods=shift | alt), "\x1b" + 'V')
        ae(enc(ord('v'), mods=ctrl), '6')
        ae(enc(ord('v'), mods=ctrl | alt), "\x1b" + '6')
        ae(enc(ord('w')), 'w')
        ae(enc(ord('w'), mods=shift), 'W')
        ae(enc(ord('w'), mods=alt), "\x1b" + 'w')
        ae(enc(ord('w'), mods=shift | alt), "\x1b" + 'W')
        ae(enc(ord('w'), mods=ctrl), '7')
        ae(enc(ord('w'), mods=ctrl | alt), "\x1b" + '7')
        ae(enc(ord('x')), 'x')
        ae(enc(ord('x'), mods=shift), 'X')
        ae(enc(ord('x'), mods=alt), "\x1b" + 'x')
        ae(enc(ord('x'), mods=shift | alt), "\x1b" + 'X')
        ae(enc(ord('x'), mods=ctrl), '8')
        ae(enc(ord('x'), mods=ctrl | alt), "\x1b" + '8')
        ae(enc(ord('y')), 'y')
        ae(enc(ord('y'), mods=shift), 'Y')
        ae(enc(ord('y'), mods=alt), "\x1b" + 'y')
        ae(enc(ord('y'), mods=shift | alt), "\x1b" + 'Y')
        ae(enc(ord('y'), mods=ctrl), '9')
        ae(enc(ord('y'), mods=ctrl | alt), "\x1b" + '9')
        ae(enc(ord('z')), 'z')
        ae(enc(ord('z'), mods=shift), 'Z')
        ae(enc(ord('z'), mods=alt), "\x1b" + 'z')
        ae(enc(ord('z'), mods=shift | alt), "\x1b" + 'Z')
        ae(enc(ord('z'), mods=ctrl), ':')
        ae(enc(ord('z'), mods=ctrl | alt), "\x1b" + ':')
# end legacy letter tests
        # }}}

        ae(enc(key=ord(' ')), ' ')
        ae(enc(key=ord(' '), mods=ctrl), '\0')
        ae(enc(key=ord('i'), mods=ctrl | shift), csi(ctrl | shift, ord('i')))

        q = partial(enc, key=ord('a'))
        ae(q(), 'a')
        ae(q(text='a'), 'a')
        ae(q(action=repeat), 'a')
        ae(q(action=release), '')

        # test disambiguate
        dq = partial(enc, key_encoding_flags=0b1)
        ae(dq(ord('a')), 'a')
        ae(dq(defines.GLFW_FKEY_ESCAPE), csi(num=27))  # esc
        for mods in (ctrl, alt, ctrl | shift, alt | shift):
            ae(dq(ord('a'), mods=mods), csi(mods, ord('a')))
        ae(dq(ord(' '), mods=ctrl), csi(ctrl, ord(' ')))
        for k in (defines.GLFW_FKEY_KP_PAGE_UP, defines.GLFW_FKEY_KP_0):
            ae(dq(k), csi(num=k))
            ae(dq(k, mods=ctrl), csi(ctrl, num=k))

    def test_encode_mouse_event(self):
        NORMAL_PROTOCOL, UTF8_PROTOCOL, SGR_PROTOCOL, URXVT_PROTOCOL = range(4)
        L, M, R = 1, 2, 3
        protocol = SGR_PROTOCOL

        def enc(button=L, action=defines.PRESS, mods=0, x=1, y=1):
            return defines.test_encode_mouse(x, y, protocol, button, action, mods)

        self.ae(enc(), '<0;1;1M')
        self.ae(enc(action=defines.RELEASE), '<0;1;1m')
        self.ae(enc(action=defines.MOVE), '<35;1;1M')
        self.ae(enc(action=defines.DRAG), '<32;1;1M')

        self.ae(enc(R), '<2;1;1M')
        self.ae(enc(R, action=defines.RELEASE), '<2;1;1m')
        self.ae(enc(R, action=defines.DRAG), '<34;1;1M')

        self.ae(enc(M), '<1;1;1M')
        self.ae(enc(M, action=defines.RELEASE), '<1;1;1m')
        self.ae(enc(M, action=defines.DRAG), '<33;1;1M')

        self.ae(enc(x=1234, y=5678), '<0;1234;5678M')
        self.ae(enc(mods=defines.GLFW_MOD_SHIFT), '<4;1;1M')
        self.ae(enc(mods=defines.GLFW_MOD_ALT), '<8;1;1M')
        self.ae(enc(mods=defines.GLFW_MOD_CONTROL), '<16;1;1M')
