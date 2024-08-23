document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const form = document.getElementById('signup-form') || document.getElementById('signin-form');
    const imageDataInput = document.getElementById('image-data');

    // Function to start video stream
    function startVideo() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
            })
            .catch(function(error) {
                console.error('Error accessing webcam:', error);
                alert('Could not access webcam. Please check your permissions and try again.');
            });
    }

    // Call the function to start video
    startVideo();

    captureButton.addEventListener('click', function() {
        if (video.srcObject) {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL('image/jpeg');
            imageDataInput.value = imageData;
        } else {
            alert('No video stream detected.');
        }
    });

    if (form) {
        form.addEventListener('submit', function(event) {
            const dataURL = imageDataInput.value;
            const byteString = atob(dataURL.split(',')[1]);
            const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0];
            const arrayBuffer = new ArrayBuffer(byteString.length);
            const uint8Array = new Uint8Array(arrayBuffer);
            for (let i = 0; i < byteString.length; i++) {
                uint8Array[i] = byteString.charCodeAt(i);
            }
            const blob = new Blob([uint8Array], { type: mimeString });

            const formData = new FormData(form);
            formData.set('image', blob, 'image.jpg');

            fetch(form.action, {
                method: form.method,
                body: formData
            }).then(response => response.text())
              .then(text => {
                  if (text.includes('Welcome back')) {
                      window.location.href = '/home';
                  } else {
                      alert('Error: ' + text);
                  }
              }).catch(error => console.error('Error:', error));

            event.preventDefault();
        });
    }
});
