$('#search-form').on('submit', (evt) => {
    evt.preventDefault();

//make this into a function and call it from both event handlers
//set a variable = loading and inside success function set it to false; if true, do nothing. otherwise make the ajax request
    $.ajax({
      url: '/api/search',
      type: 'POST', //make this a POST request
      data: {
        keywords: $('#keywords').val(),
        order: $('#order').val(),
        // max_results: $('#max-results').val(),
        published_before: $('#published-before').val(),
        published_after: $('#published-after').val(),
        min_subscriber_count: $('#min-subscribers').val(),
        max_subscriber_count: $('#max-subscribers').val()
        //can include another parameter here for the results page
      },
      success: function(response) {
          let trHTML = '';
          $.each(response, function (i, item) {
            for (channel of item) {
              trHTML += `<tr><td> ${channel.title} </td>
              <td> ${channel.description} </td>
              <td> ${channel.video_count} </td>
              <td> ${channel.view_count} </td>
              <td> ${channel.subscriber_count} </td>
              <td> ${(channel.email).join("\n")} </td>
              <td> <a target='_blank' href=${channel.url}>Link</a></td>
              <td> <button type="button" class="btn btn-primary btn-sm btn-success" id="button-add">Add</button><br>

              </tr>`;
            }
          });
          $('#results-table').append(trHTML);
      }
  });
});

$('#next-page').on('click', (evt) => {
    evt.preventDefault();

    $.ajax({
      url: '/api/search',
      type: 'POST', //make this a POST request
      data: {
        keywords: $('#keywords').val(),
        order: $('#order').val(),
        max_results: $('#max-results').val(),
        published_before: $('#published-before').val(),
        published_after: $('#published-after').val(),
        min_subscriber_count: $('#min-subscribers').val(),
        max_subscriber_count: $('#max-subscribers').val()
        //can include another parameter here for the results page
      },
      success: function(response) {
        let trHTML = '';
        $.each(response, function (i, item) {
          for (channel of item) {
            trHTML += `<tr><td> ${channel.title} </td>
            <td> ${channel.description} </td>
            <td> ${channel.video_count} </td>
            <td> ${channel.view_count} </td>
            <td> ${channel.subscriber_count} </td>
            <td> ${(channel.email).join("\n")} </td>
            <td> <a target='_blank' href=${channel.url}>Link</a></td>
            <td> <button type="button" class="btn btn-primary btn-sm btn-success" id="button-add">Add</button><br>

            </tr>`;
          }
        });
        $('#results-table').append(trHTML);
    }
});
});