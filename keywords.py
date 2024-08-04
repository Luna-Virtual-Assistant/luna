
keywords = {
    'play': [
        'toque',
        'tocar',
        'reproduzir'
    ], 
    'pause': [
        'pause',
        'pausar',
        'parar',
        'pare',  
    ],
    'continue': [
        'continue',
        'continuar',
        'retomar',
        'prosseguir',
        'prossiga',
        'retome',
        'despause',
        'despausar',
    ],
    'next': [
        'próximo',
        'avançar',
        'avançar para o próximo',
        'próxima',
        'próximo vídeo',
        'próximo por favor',
        'próximo por favor',
        'próximo vídeo por favor',
        'próxima música'
    ],
    'previous': [
        'anterior',
        'voltar',
        'voltar para o anterior',
        'anterior',
        'anterior vídeo',
        'anterior por favor',
        'anterior por favor',
        'anterior vídeo por favor',
        'anterior música'
    ],
    'mute': [
        'mute',
        'mudo',
        'silenciar',
        'silencie',
        'silencie por favor',
        'silenciar por favor',
        'mudo por favor',
        'mude por favor',
    ]
    
}

keyword_mapping = {kw: action for action, keywords in keywords.items() for kw in keywords}   