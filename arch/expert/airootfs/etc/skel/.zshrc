# Tunudan OS Expert — zsh
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt share_history hist_ignore_dups autocd
bindkey -e
autoload -Uz compinit && compinit
[ -f /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ] && \
    . /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
[ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ] && \
    . /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
alias ls='ls --color=auto' ll='ls -lah' v='nvim' maj='tunudan-update'
command -v starship >/dev/null && eval "$(starship init zsh)"
[ -z "$TUNUDAN_FETCH_DONE" ] && export TUNUDAN_FETCH_DONE=1 && \
    fastfetch -c /usr/share/tunudan/fastfetch/config.jsonc 2>/dev/null
