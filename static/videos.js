$('#search-form').on('submit', (evt) => {
    evt.preventDefault();
  
    // TODO: Serialize this if you have time
    const formData = {
      keywords: $('#keywords').val(),
      order: $('#order').val(),
      max_results: $('#max-results').val(),
      published_before: $('#published-before').val(),
      published_after: $('#published-after').val()

    };

    // Send formData to the server (becomes a query string)
    $.get('/api/search', formData, (res) => {
      // Display response from the server
      $('#results').text(res)
    });
  });

  console.log("done")