set number
set relativenumber
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'tpope/vim-surround'
Plugin 'junegunn/fzf'
Plugin 'junegunn/fzf.vim'
Plugin 'valloric/youcompleteme' " requires vim with python support
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'airblade/vim-gitgutter'
Plugin 'bling/vim-airline'
Plugin 'altercation/vim-colors-solarized'
Plugin 'scrooloose/nerdtree'



" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
syntax enable

set tabstop=4
set list listchars=tab:▸\ ,eol:¬,trail:·
set list
let g:solarized_termcolors=256
set background=dark
colorscheme solarized
