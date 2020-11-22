

//Submit keywords and print results to table

$('#search-form').on('submit', (evt) => {
    evt.preventDefault();
    $("#results-table tbody tr").remove();

    // if ($('#keyword-video').text().trim() === "Select") {
    //   evt.preventDefault();
    //   alert("Please select a video or keyword search");
    // }
    
    $.ajax({
      url: '/api/search',
      type: 'POST', //make this a POST request
      data: {
        keywords: $('#keywords').val(),
        // order: $('#order').val(),
        // max_results: $('#max-results').val(),
        type: $('#keyword-video').text().trim(),
        min_subscriber_count: $('#min-subscribers').val(),
        max_subscriber_count: $('#max-subscribers').val(),
        title_keywords: $('#title-contains').val(),
        desc_keywords: $('#desc-contains').val()
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
        title_keywords: $('#title-contains').val(),
        desc_keywords: $('#desc-contains').val(), 
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
      alert('Successfully added')
      location.reload(true)
      // $('.modal-body').html("Successfully added");
      // $('#dropdown-menu').append(`<li><a>${response}</a></li>`);
  
      // $.each(response, function (i, item) {
      //     console.log(response)
        
  }
});
});

//Reset the modal once submitted

$("#exampleModal").on("hidden.bs.modal", function(){
  $(".modal-body").html(`<label for="recipient-name" class="col-form-label" id="title_title">Title</label>
  <input type="text" class="form-control" id="list_title">`);
});


//Update Dropdown list with Selected List Title

$("#dropdown-menu li a").click(function(){
  
  $("#dropdown-list:first-child").html($(this).text()+' <span class="caret"></span>');
  
});

//Update Main page dropdown with Keyword or Video

$("#keyword-video-dropdown li a").click(function(){
  
  $("#keyword-video:first-child").html($(this).text()+' <span class="caret"></span>');
  
});

//Add Influencer to List when Add Button is Clicked

// $("#add-button").click(function(){
  
//   $.ajax({
//     url: '/api/add_influencer',
//     type: 'POST', //make this a POST request
//     data: {
//       list_title: $('#list_title').val(),
//       $(this).closest("tr")
//     },
//     success: function(response) {
//       $('.modal-body').html("Successfully added");
//       $('#dropdown-menu').append(`<li><a>${response}</a></li>`);
//       $.each(response, function (i, item) {
//           console.log(response)
// ;
        
//       });
//       $('#results-table').append(trHTML);
//   }
// });
// });

$(document).on("click", "#button-add", function(){
  if ($('#dropdown-list').text().trim() === "Select a List") {
    alert("Please select a list");
  
  } else {
  let row = $(this).closest("tr");
  let value = row.find("td");
  let link = row.find("td:nth-child(7)").children().attr('href')
  let row_data_obj = {}
  let row_data_obj_keys = ["title", "description", "video_count", "view_count", "sub_count", "email"]


  for (key of row_data_obj_keys) {
    row_data_obj[key] = row.find(`td:nth-child(${row_data_obj_keys.indexOf(key) + 1})`).text().trim();
  }

  row_data_obj["link"] = link

  

  $.ajax({
        url: '/api/add_influencer',
        type: 'POST', //make this a POST request
        data: {
          list_title: $('#dropdown-list').text().trim(),
          row_data: row_data_obj
        },
        success: function(response) {
          row.find("td:nth-child(8)").html(`<button type="button" class="btn btn-primary btn-sm btn-danger" id="button-remove">Remove</button>`);
            
          }
    });
  }});

  //Enrich Profiles
$(document).on("click", "#enrich", function(){
  $("#enrich").text("Loading...")
  let channel_titles = [];
  
  let rows = document.querySelectorAll("#profile-table tr");
  
  for (var i = 1; i < rows.length; i++) {
    let row = [], cols = rows[i].querySelectorAll("td, th");
    let col = (`${cols[0].innerText}`.replace(",", "\,"));
    let obj = {};
    obj["title"] = col;
    console.log(obj);
    row.push(obj);
    
        // for (var j = 0; j < 1; j++) {
        //       let col = (`${cols[j].innerText}`.replace(",", "\,"));
              // obj["title"] = col
              // console.log(obj)
              // row.push(obj);

    channel_titles.push(obj)
    console.log(row)
    console.log(channel_titles)		

  }
  
  $.ajax({
        url: '/api/enrich',
        type: 'POST', //make this a POST request
        data: {
          channel_titles: JSON.stringify(channel_titles)
        },
        success: function(response) {
          $("#enrich").text("Enrich Profiles")
          let i = 0
          // $('#first-row').append('<th>IG Username</th>')
          // $(this).find('th').eq(6).after('<th>IG Username</th>');
          $('#first-row').children().eq(6).after('<th>IG Username</th>');
          $('#first-row').children().eq(7).after('<th>IG Followers</th>');
          
          $('#profile-table').find('tr').each(function(index){
            // $(this).find('th').eq(6).after('<th>IG Username</th>');
            // console.log($('#profile-table').index('tr'))
            if (index != 0) {
              let trHTML = ""
              trHTML += `<td>${response[i].ig_username}</td>`
              trHTML += `<td>${response[i].ig_followers}</td>`
              console.log(trHTML)

              $(this).find('td').eq(6).after(trHTML);
              i += 1
            } 
          
          }
          )
        }
      }
    );
    });


  //Remove influencer from a list 

  $(document).on("click", "#button-remove", function(){
    if ($('#dropdown-list').text().trim() === "Select a List") {
      alert("Please select a list");
    
    } else {
    let row = $(this).closest("tr");
    let title = row.find("td:nth-child(1)").text().trim();
    
  
    $.ajax({
          url: '/api/remove_influencer',
          type: 'POST', //make this a POST request
          data: {
            list_title: $('#dropdown-list').text().trim(),
            channel_title: title
          },
          success: function(response) {
            row.find("td:nth-child(8)").html(`<button type="button" class="btn btn-primary btn-sm btn-success" id="button-add">Add</button>`);
              
            }
      });
    }});

//Remove influencer from list on profile

    $(document).on("click", "#button-remove-profile", function(){
      let row = $(this).closest("tr");
      let title = row.find("td:nth-child(1)").text().trim();

      $.ajax({
        url: '/api/remove_influencer',
        type: 'POST', //make this a POST request
        data: {
          list_title: $('#profile-list').text().trim(),
          channel_title: title
        },
        success: function(response) {
          row.remove();
            
          }
    });
  });

//Update Profile list dropdown with title & request influencer data
$("#menu-profile li a").click(function(){
  
  $("#profile-list:first-child").html($(this).text()+' <span class="caret"></span>');
  $("#profile-table tbody tr").remove(); 

  $.ajax({
    url: '/api/load_lists',
    type: 'POST', //make this a POST request
    data: {
      list_title: $('#profile-list').text().trim(),
    },
    success: function(response) {
      let trHTML = '';
      // $.each(response, function (i, item) {
        for (channel of response.channels) {
          trHTML += `<tr><td> ${channel.title} </td>
          <td> ${channel.description} </td>
          <td> ${channel.video_count} </td>
          <td> ${channel.view_count} </td>
          <td> ${channel.subscriber_count} </td>
          <td> ${(channel.email)} </td>
          <td> <a target='_blank' href=${channel.url}>Link</a></td>
          <td> <button type="button" class="btn btn-primary btn-sm btn-danger" id="button-remove-profile">Remove</button><br>
          </tr>`;
        }
      // });
      $('#profile-table').append(trHTML);
        
      }
    });
});

//Export Table to CSV

function download_csv(csv, filename) {
  let csvFile;
  let downloadLink;

  // CSV FILE
  csvFile = new Blob([csv], {type: "text/csv"});

  // Download link
  downloadLink = document.createElement("a");

  // File name
  downloadLink.download = filename;

  // We have to create a link to the file
  downloadLink.href = window.URL.createObjectURL(csvFile);

  // Make sure that the link is not displayed
  downloadLink.style.display = "none";

  // Add the link to your DOM
  document.body.appendChild(downloadLink);

  // Lanzamos
  downloadLink.click();
}

// function export_results_table_to_csv(html, filename) {
// let csv = [];
// let rows = document.querySelectorAll("#results-table tr");
// console.log(rows)

//   for (var i = 0; i < rows.length; i++) {
//   let row = [], cols = rows[i].querySelectorAll("td, th");
//   console.log(row)
  
//       for (var j = 0; j < 10; j++) 
//           if (j = 7) { 
//             row.push(`"${cols[j].children().attr('href')}"`)
//           } else {
//           row.push(`"${cols[j].innerText}"`);
//           }


//       //escape all commas
//       //string replace with \,
//       row = row.replace(",", "\,")
      
//   csv.push(row.join(","));		
// }

//   // Download CSV
//   download_csv(csv.join("\n"), filename);
// }


function export_table_to_csv(html, filename, table_name) {
  let csv = [];
  let rows = document.querySelectorAll(`${table_name} tr`);
  console.log(rows)
  
    for (var i = 0; i < rows.length; i++) {
    let row = [], cols = rows[i].querySelectorAll("td, th");
    console.log(row)
    
        for (var j = 0; j < cols.length; j++) 
            if (j === 6 && i > 0) { 
              row.push(cols[j].lastElementChild.getAttribute("href"))
            } else {
              let col = (`"${cols[j].innerText}"`.replace(",", "\,"));
              row.push(col);
          }
  
        
    csv.push(row.join(","));		
  }
  
    // Download CSV
    download_csv(csv.join("\n"), filename);
  }

document.querySelector("#export").addEventListener("click", function (evt) { //targetattribute = button that was clicked that resulted in event
  var html = document.querySelector("#profile-table").outerHTML;
export_table_to_csv(html, "results.csv", "#profile-table");
});

document.querySelector("#export").addEventListener("click", function () {
  var html = document.querySelector("#results-table").outerHTML;
export_table_to_csv(html, "results.csv", "#results-table");
});


// //Sort the table by the header
// $(document).ready(function () {
//   $('#results-table').DataTable({
//   "ordering": false // false to disable sorting (or any other option)
//   });
//   $('.dataTables_length').addClass('bs-select');
//   });


// Load all users lists

// $(document).on("click", "#load-lists", function(){
  
//   $.ajax({
//     url: '/api/load_lists',
//     type: 'POST', //make this a POST request
//     data: {
//     },
//     success: function(response) {
//       let tableHTML = ""
//       for (lst of response) {
//         tableHTML += `<tr><td> ${lst.list_id} </td>
//             <td> ${lst.list_title} </td>
//             <td> <button type="button" class="btn btn-primary btn-sm btn-success" id="remove-list">Remove</button><br>
//             </tr>`
//       }
//       $('#page-content-wrapper').append(tableHTML)
//       }

// (function ($){
//   $.fn.counter = function() {
//     const $this = $(this),
//     numberFrom = parseInt($this.attr('data-from')),
//     numberTo = parseInt($this.attr('data-to')),
//     delta = numberTo - numberFrom,
//     deltaPositive = delta > 0 ? 1 : 0,
//     time = parseInt($this.attr('data-time')),
//     changeTime = 10;
    
//     let currentNumber = numberFrom,
//     value = delta*changeTime/time;
//     var interval1;
//     const changeNumber = () => {
//       currentNumber += value;
//       //checks if currentNumber reached numberTo
//       (deltaPositive && currentNumber >= numberTo) || (!deltaPositive &&currentNumber<= numberTo) ? currentNumber=numberTo : currentNumber;
//       this.text(parseInt(currentNumber));
//       currentNumber == numberTo ? clearInterval(interval1) : currentNumber;  
//     }

//     interval1 = setInterval(changeNumber,changeTime);
//   }
// }(jQuery));

// $(document).ready(function(){

//   $('.count-up').counter();
//   $('.count1').counter();
//   $('.count2').counter();
//   $('.count3').counter();
  
//   new WOW().init();
  
//   setTimeout(function () {
//     $('.count5').counter();
//   }, 3000);
// });
  