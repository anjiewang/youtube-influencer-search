

//Submit keywords and print results to table

$('#search-form').on('submit', (evt) => {
    evt.preventDefault();

    $.ajax({
      url: '/api/search',
      type: 'POST', //make this a POST request
      data: {
        keywords: $('#keywords').val(),
        order: $('#order').val(),
        // max_results: $('#max-results').val(),
 
        min_subscriber_count: $('#min-subscribers').val(),
        max_subscriber_count: $('#max-subscribers').val()
        //can include another parameter here for the results page
      },
      success: function(response) {
          let trHTML = '';
          // $.each(response, function (i, item) {
            nextPageToken = response.tokens.nextPageToken;
            for (channel of response.channels) {
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
          // });
          $('#results-table').append(trHTML);
      }
  });
});

//On next page, call server and add results to table

$('#next-page').on('click', (evt) => {
    evt.preventDefault();

    $.ajax({
      url: '/api/search',
      type: 'POST', //make this a POST request
      data: {
        keywords: $('#keywords').val(),
        order: $('#order').val(),
        max_results: $('#max-results').val(),
        // published_before: $('#published-before').val(),
        // published_after: $('#published-after').val(),
        min_subscriber_count: $('#min-subscribers').val(),
        max_subscriber_count: $('#max-subscribers').val(), 
        next_page_token: nextPageToken
        //can include another parameter here for the results page
      },
      success: function(response) {
        let trHTML = '';
        // $.each(response, function (i, item) {
          nextPageToken = response.tokens.nextPageToken
          for (channel of response.channels) {
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
        // });
        $('#results-table').append(trHTML);
    }
});
});



//Save list and add to dropdown menu

$('#save_list').on('click', (evt) => {
  evt.preventDefault();

  $.ajax({
    url: '/api/add_list',
    type: 'POST', //make this a POST request
    data: {
      list_title: $('#list_title').val(),
    },
    success: function(response) {
      $('.modal-body').html("Successfully added");
      $('#dropdown-menu').append(`<li><a>${response}</a></li>`);
      $.each(response, function (i, item) {
          console.log(response)
        
      });
  }
});
});

//Reset the modal once submitted

$("#exampleModal").on("hidden.bs.modal", function(){
  $(".modal-body").html(`<label for="recipient-name" class="col-form-label" id="title_title">Title</label>
  <input type="text" class="form-control" id="list_title">`);
});


//Update Dropdown list with Selected List Title

$(".dropdown-menu li a").click(function(){
  
  $("#dropdown-list:first-child").html($(this).text()+' <span class="caret"></span>');
  
});

//Add Influencer to List when Add Button is Clicked

$("#add-button").click(function(){
  
  $.ajax({
    url: '/api/add_list',
    type: 'POST', //make this a POST request
    data: {
      list_title: $('#list_title').val(),
    },
    success: function(response) {
      $('.modal-body').html("Successfully added");
      $('#dropdown-menu').append(`<li><a>${response}</a></li>`);
      $.each(response, function (i, item) {
          console.log(response)
;
        
      });
      $('#results-table').append(trHTML);
  }
});
});
