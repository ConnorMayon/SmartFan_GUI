self.addEventListener('message', function(e) {
  // code to be run
  while(true)
  {
	  fetch('/log')
          .then(response => response.json())
          .then(data => {
              if (data.length !== 0) {
               updateContent(data);
              }
          })
          .catch(error => console.error('Error fetching data:', error));

  }
}