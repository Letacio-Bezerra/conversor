const express = require('express');
const fileUpload = require('express-fileupload');
const ffmpeg = require('fluent-ffmpeg');
const path = require('path');
const app = express();

app.use(express.static('public'));
app.use(fileUpload());

app.post('/convert', (req, res) => {
    if (!req.files || Object.keys(req.files).length === 0) {
        return res.status(400).send({ message: 'Nenhum arquivo foi enviado.' });
    }

    const file = req.files.file;
    const outputPath = path.join(__dirname, 'uploads', `${Date.now()}.mp3`);

    ffmpeg(file.data)
        .toFormat('mp3')
        .on('end', () => {
            res.send({ message: 'Conversão concluída com sucesso!' });
        })
        .on('error', (err) => {
            console.error(err);
            res.status(500).send({ message: 'Erro ao converter o arquivo.' });
        })
        .save(outputPath);
});

app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000.');
});
