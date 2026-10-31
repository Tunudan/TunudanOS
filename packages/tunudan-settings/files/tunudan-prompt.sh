# shellcheck shell=sh
# Tunudan OS — invite de commande et accueil du terminal
case $- in *i*) ;; *) return 0 2>/dev/null || exit 0 ;; esac
if [ -n "$BASH_VERSION" ]; then
    PS1='\[\e[38;5;208m\]\u@\h\[\e[0m\]:\[\e[38;5;250m\]\w\[\e[0m\]\$ '
fi
if [ -z "$TUNUDAN_FETCH_DONE" ] && command -v fastfetch >/dev/null 2>&1 \
   && [ -f /usr/share/tunudan/fastfetch/config.jsonc ] && [ ! -f "$HOME/.hushlogin" ]; then
    export TUNUDAN_FETCH_DONE=1
    fastfetch -c /usr/share/tunudan/fastfetch/config.jsonc 2>/dev/null
fi
