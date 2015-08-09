# Vintage YankStack

>   A yankstack (or Emacs Kill Ring equivalent) for ST3's Vintage

## What is it?
One of the killer features from `Emacs` is `Kill Ring`, which allow to paste the *previous of previous* killed (or yanked, deleted in Vim style) in place *previous* paste region. That means, no clipboard selection, no `:ls` and no `undo`.

`Sublime Text` introduces a kill ring compatible with Emacs but it doesn't do what it should do, especially with Vintage, so I wrote it my self. The idea (and name) from the excellent [YankStack](https://github.com/maxbrunsfeld/vim-yankstack) plugin for Vim which is lightweight and elegant.

## Install
### Via package control (Recommended)
<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd>, `Install Packagee`, then `YankStack` to install.

### Manual
Clone [this repo](https://github.com/linktohack/VintageYankStack) to your Packages directory, modify the keymap if needed.

## Usage
Default keymaps are:
- <kbd>CTRL</kbd>+<kbd>P</kbd>: Paste from higher register in stack
- <kbd>CTRL</kbd>+<kbd>N</kbd>: Paste from lower register in stack

No worrier about key conflict, the above keymaps work only if the last action was a *paste*, or *yankstack it self*, see keymap file for details.

So a normal work routine is like this:

1. Copy (<kbd>y</kbd>), delete(<kbd>d</kbd>), change(<kbd>c</kbd>) in serveral place.
2. Move to the place you need to paste some of those.
3. Paste (<kbd>p</kbd>, <kbd>P</kbd>), if it not what you want, just hit <kbd>CTRL</kbd>+<kbd>P</kbd> to cycle the registers back to what you need, if you miss it, hit <kbd>CTRL</kbd>+<kbd>N</kbd> to cycle them forward.

## License
MIT