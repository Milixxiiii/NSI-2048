<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>2048 - Naïl, Milo & Merwan</title>
<style>
  body {
    background: linear-gradient(120deg, #f6d365, #fda085);
    font-family: 'Arial', sans-serif;
    text-align: center;
    padding: 50px;
    color: #333;
  }

  h1 {
    font-size: 2.5em;
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glow 2s infinite alternate;
  }

  @keyframes glow {
    from { text-shadow: 0 0 5px #ff6a00, 0 0 10px #ee0979; }
    to { text-shadow: 0 0 20px #ff6a00, 0 0 30px #ee0979; }
  }

  img {
    width: 200px;
    height: 200px;
    border-radius: 20px;
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
  }

  img:hover {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
  }

  p {
    font-size: 1.2em;
  }
</style>
</head>
<body>

<h1>Bienvenue sur le dépôt du jeu <strong>2048</strong></h1>
<p>Développé par <strong>Naïl, Milo et Merwan</strong></p>

<p align="center">
  <img alt="Aperçu du jeu 2048" src="https://github.com/user-attachments/assets/f0c243e7-6cf2-4bc5-8ba1-7c28d83a1ab1" />
</p>

</body>
</html>
