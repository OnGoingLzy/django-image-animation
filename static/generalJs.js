
function logout(){
        $.ajax({
          url: '/api/logout/',
          method: 'get',
          processData: false,
          success: function(response) {
            window.location.href = '/sign-in/';
          },
          error: function(xhr, status, error) {
            alert(xhr.responseText);
          }
        });
      }