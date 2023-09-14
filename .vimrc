call plug#begin()

Plug 'preservim/nerdtree', { 'on': 'NerdTreeToggle' }
Plug 'easymotion/vim-easymotion'
Plug 'airblade/vim-gitgutter'
Plug 'frazrepo/vim-rainbow'
Plug 'dense-analysis/ale'

call plug#end()

set splitright
set splitbelow
set history=100
syntax on
set autoindent
set tabstop=4
set shiftwidth=4
set expandtab

function ToggleLine()
	if &nu == 0
		set nu
	elseif &rnu == 0
		set rnu
	else
		set nonu
		set nornu
	endif
endfunction

let mapleader=" "
map<leader>q :q<Return>
map<leader>s :w<Return>
map<leader>l :call ToggleLine()<Return>
map<leader>c :g++ -Wall -O2 -std=c++14 -o %< %<Return>
map<leader>h :ALEToggle<Return>

inoremap ' ''<Left>
inoremap " ""<Left>
inoremap ( ()<Left>
inoremap [ []<Left>
inoremap { {}<Left>

