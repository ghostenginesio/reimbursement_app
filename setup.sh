mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#086262'
backgroundColor='#097b65'
secondaryBackgroundColor='#0f1010'
textColor='#fbf3f3'
font='serif'

[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml