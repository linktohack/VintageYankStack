# VintageYankStack

>   A yankstack (or Emacs Kill Ring equivalent) for ST3's Vintage

## What is it?
One of the killer features from Emacs is Kill Ring, which will paste the *previous of previous* killed (or yanked, deleted in Vim style) in place *previous* paste region. That means, no clipboard selection, no `:ls` and no `undo`.

Sublime introduce kill ring compatible with Emacs but it doesn't do what it should do, especially with Vintage, so I wrote it my self. The idea (and name) from the excellent [YankStack](https://github.com/maxbrunsfeld/vim-yankstack) plugin for Vim which is lightweight and elegant.


## Requirement
<strike>This plugin need Vintage with supporting of numbered registers to work, since it cycle through those registers [0-9].</strike>

<strike>I've fired a pull request to @sublimehq, but for now just clone my Vingtage fork from [here](https://github.com/linktohack/Vintage) or patch/edit the vintage.py itself, like [this gist](https://gist.github.com/linktohack/5656883): it's just *less than 10 lines*</strike>

Since there is no response from Jon for the patch to be merged, I override some `Command`s in Vintage. The advantage is we will have more `vim`-like behavior, with the registers are rotated whenever an unname one is pushed.

## Usage
Clone [this repo](https://github.com/linktohack/VintageYankStack) to your Packges directory, modify the keymaps if needed.

Default keymaps are:

- <kbd>ctrl</kbd>+<kbd>P</kbd>: Paste from higher register in stack
- <kbd>ctrl</kbd>+<kbd>N
</kbd>: Paste from lower register in stack

No worrier about key conflict, the above keymaps work only if the last action was a *paste*, or *yankstack it self*, see keymap file for details.

So a normal work routine is like this:

1. Copy (<kbd>y</kbd>), delete(<kbd>d</kbd>), change(<kbd>c</kbd>) in serveral place.
2. Move to the place you need to paste some of those.
3. Paste (<kbd>p</kbd>, <kbd>P</kbd>), if it not what you want, just hit <kbd>ctrl</kbd>+<kbd>P</kbd> to cycle the registers back to what you need, if you miss it, hit <kbd>ctrl</kbd>+<kbd>N</kbd> to cycle them forward.

## License
MIT