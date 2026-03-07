import streamlit as st
import time
import random

st.set_page_config(page_title="I-5 Patrol Flappy", layout="wide")

# Custom CSS for game style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

    .betts-yell {
        background: #ff0000;
        color: #ffff00;
        font-family: 'Bangers', cursive;
        font-size: 48px;
        text-align: center;
        padding: 30px;
        border: 8px solid #000;
        border-radius: 15px;
        margin: 20px 0;
        text-shadow: 3px 3px 6px #000;
        box-shadow: 0 0 20px #ff4500;
    }

    .betts-face {
        display: block;
        margin: 0 auto 15px;
        border: 5px solid #ffd700;
        border-radius: 50%;
        box-shadow: 0 0 20px #ff4500;
    }

    .game-container {
        margin: 0 auto;
        width: 400px;
    }
    </style>
""", unsafe_allow_html=True)

# Lt. Betts angry image
BETTS_IMG = "https://media.istockphoto.com/id/1385108467/vector/angry-army-bootcamp-drill-sergeant-cartoon.jpg?s=612x612&w=0&k=20&c=3fGMt7aLzLa0uRGSZREujosQhE77PNWVKPpH6849GFo="

st.title("🚔 I-5 Patrol Flappy – Avoid Debris & Cars!")

st.image(BETTS_IMG, width=280, caption="Lt. Scott Betts – FURIOUS!", use_column_width=False, clamp=False, channels="RGB", class_="betts-face")

st.markdown(f'<div class="betts-yell">{st.session_state.get("message", "GET THOSE SPEEDERS, TROOPER!")}</div>', unsafe_allow_html=True)

# Full HTML for the Flappy Bird-like game (themed as patrol car avoiding debris/cars)
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>I-5 Patrol Flappy</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #87CEEB;
        }
        #game-container {
            position: relative;
            width: 400px;
            height: 600px;
            background-color: #FFFFFF;
            overflow: hidden;
        }
        #patrol-car {
            position: absolute;
            width: 50px;
            height: 30px;
            background-color: #0000FF;
            border-radius: 5px;
        }
        .obstacle {
            position: absolute;
            width: 60px;
            background-color: #A9A9A9;
            outline: none;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="patrol-car"></div>
    </div>
    <script>
        const container = document.getElementById("game-container");
        const car = document.getElementById("patrol-car");
        let carTop = 250;
        let carLeft = 50;
        let gravity = 2;
        let gameSpeed = 2;
        let isGameOver = false;
        let score = 0;
        let obstacles = [];

        function jump() {
            if (!isGameOver) {
                carTop -= 50;
            }
        }

        document.addEventListener("keydown", (e) => if (e.code === 'Space') jump(););
        document.addEventListener("click", jump);

        function createObstacle() {
            const topHeight = Math.random() * 200 + 50;
            const bottomTop = topHeight + 200;  // Gap of 200
            const bottomHeight = container.clientHeight - bottomTop;

            const topObstacle = document.createElement("div");
            topObstacle.classList.add("obstacle");
            topObstacle.style.height = topHeight + "px";
            topObstacle.style.top = "0px";
            topObstacle.style.left = "400px";
            container.appendChild(topObstacle);

            const bottomObstacle = document.createElement("div");
            bottomObstacle.classList.add("obstacle");
            bottomObstacle.style.height = bottomHeight + "px";
            bottomObstacle.style.top = bottomTop + "px";
            bottomObstacle.style.left = "400px";
            container.appendChild(bottomObstacle);

            obstacles.push(topObstacle, bottomObstacle);
        }

        function updateObstacles() {
            for (let i = 0; i < obstacles.length; i++) {
                let left = parseInt(obstacles[i].style.left);
                left -= gameSpeed;
                obstacles[i].style.left = left + "px";

                if (left < -60) {
                    obstacles[i].remove();
                    obstacles.splice(i, 1);
                    i--;
                    score += 0.5;  // Half point per obstacle pair
                }
            }
        }

        function checkCollision() {
            const carRect = car.getBoundingClientRect();
            for (let obstacle of obstacles) {
                const obsRect = obstacle.getBoundingClientRect();
                if (
                    carRect.right > obsRect.left &&
                    carRect.left < obsRect.right &&
                    carRect.bottom > obsRect.top &&
                    carRect.top < obsRect.bottom
                ) {
                    isGameOver = true;
                }
            }
        }

        function gameLoop() {
            if (!isGameOver) {
                carTop += gravity;
                car.style.top = carTop + "px";

                updateObstacles();
                checkCollision();

                if (carTop <= 0 || carTop >= 560) {
                    isGameOver = true;
                }

                if (Math.random() < 0.02) {
                    createObstacle();
                }

                requestAnimationFrame(gameLoop);
            } else {
                alert("Game Over! Score: " + Math.floor(score));
            }
        }

        createObstacle();
        gameLoop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=650, scrolling=False)

# Update Betts yelling periodically
if st.session_state.game_running:
    if random.random() < 0.1:
        st.session_state.message = random.choice(yells)
        st.rerun()
