window.addEventListener('load', function() {
    console.log(123)
    document.querySelector('input[type="file"]').addEventListener('change', function() {
        console.log(321)
        if (this.files && this.files[0]) {
            console.log('111')
            var img = document.getElementById('myImg');
            img.style.visibility = 'visible';
            img.onload = () => {
                URL.revokeObjectURL(img.src);  // no longer needed, free memory
            }
  
            img.src = URL.createObjectURL(this.files[0]); // set src to blob url
        }
    });
  });