
var dep = '{{ depart }}';
var arr = '{{ arrivee }}';
var tags = '{{ tags }}';
var recom = '{{ test }}';
var escales= ['{{ test[0][0] }}', '{{ test[1][0] }}', '{{ test[2][0] }}', '{{ test[3][0] }}']
function initMap() {

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          //center: ('Amiens, France')
        });
        
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer({
          draggable: true,
          map: map,
          panel: document.getElementById('right-panel'),
          suppressMarkers : false
        });
  
        directionsDisplay.addListener('directions_changed', function() {
        });

        displayRoute(dep, arr, directionsService,
            directionsDisplay);
                
}
      function displayRoute(origin, destination, service, display) {
        var waypts=[];
        for (var i = 0; i < escales.length ; i++) { 
          if (!escales[i]) {
              // si l'escale n'existe pas on n'ajoute rien a waypts
              waypts=waypts;
          } else {
              waypts.push({
                  location: escales[i]
              });
          }         
        }
        service.route({
          origin: origin,
          destination: destination,
          waypoints: waypts,
          travelMode: 'DRIVING',
          avoidTolls: true,
          optimizeWaypoints: true
        }, function(response, status) {
          if (status === 'OK') {
            display.setDirections(response);
            alert('{{ tags }}')
          } else {
            alert('Could not display directions due to: ' + status);
          }
        });
      }

    async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB8pxsl2jFQSwshMT2I5Weue8CKLgxalY8&callback=initMap">
 