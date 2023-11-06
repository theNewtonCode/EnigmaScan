const intro = document.getElementById('intro');
const imageFolder = ["{{ url_for('static', filename='imgs/image1.jpg') }}", "{{ url_for('static', filename='imgs/image2.jpg') }}", "{{ url_for('static', filename='imgs/image3.jpg') }}"];
let currentIndex = 0;

function changeBackgroundImage() {
    currentIndex = (currentIndex + 1) % imageFolder.length;
    const nextImage = imageFolder[currentIndex];
    intro.style.backgroundImage = `url('${nextImage}')`;
}

setInterval(changeBackgroundImage, 5000); // Change the background image of #intro every 5 seconds (5000 milliseconds)
