<?php
// Define que esse arquivo vai cuspir um JSON para o seu site ler
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$diretorio = 'musicas/';
$playlist = [];

// Procura todos os arquivos .mp3 dentro da pasta "musicas"
$arquivos = glob($diretorio . '*.mp3');

if ($arquivos) {
    foreach ($arquivos as $arquivo) {
        // MÁGICA: Estima a duração da música baseado no tamanho do arquivo.
        // Assumindo que os seus MP3 tenham qualidade 128kbps (que é o padrão ideal e leve pra web).
        // 128 kbps = 16.000 bytes por segundo.
        $tamanho_bytes = filesize($arquivo);
        $duracao_segundos = ceil($tamanho_bytes / 16000); 

        // Formata o nome para ficar bonito no site (tira o .mp3 e os traços)
        $nome_limpo = str_replace(['.mp3', '_', '-'], [' ', ' ', ' '], basename($arquivo));
        $nome_limpo = ucwords($nome_limpo);

        $playlist[] = [
            'name' => $nome_limpo,
            'src' => $arquivo,
            'duration' => $duracao_segundos
        ];
    }
}

// Entrega a lista pronta e calculada para o JavaScript do seu site
echo json_encode($playlist);
?>
