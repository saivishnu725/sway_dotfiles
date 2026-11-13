-- leader key to Space
vim.g.mapleader = " "

-- basic
vim.opt.number = true
vim.opt.relativenumber = true

vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4

vim.opt.mouse = "" -- should to see if i want a mouse or not

vim.opt.clipboard = "unnamedplus"

-- load lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    {
        "catppuccin/nvim",
        name = "catppuccin",
        priority = 1000
    },
    {
		"neovim/nvim-lspconfig",
		config = function()
			vim.lsp.enable("clangd")
		end
	},
	{
		"nvim-lua/plenary.nvim"
	},
	{
		"tpope/vim-fugitive"
	}
})

vim.api.nvim_create_autocmd("FileType", {
    pattern = {"c", "lua"},
    callback = function()
        vim.treesitter.start()
    end,
})

-- useful bindings
local map = vim.keymap.set

map("n", "K", vim.lsp.buf.hover)
map("n", "gb", vim.lsp.buf.definition)
map("n", "gD", vim.lsp.buf.declaration)
map("n", "gr", vim.lsp.buf.references)
map("n", "<leader>rn", vim.lsp.buf.rename)

map("n", "[d", vim.diagnostic.goto_prev)
map("n", "]d", vim.diagnostic.goto_next)

vim.keymap.set("n", "<leader>r", function()
    vim.cmd("write")
    vim.cmd("split")
    vim.cmd("terminal gcc  -Wall -Wextra -Wpedantic -fsanitize=address -g % -o %:p:h/output/%:t:r && %:p:h/output/%:t:r")
 end)
