var markers = [];
var newMarker;

function openDetails(url, category, time, description) {
    // Open the Side Window
    document.getElementById("sideDetails").style.width = "630px";

    // Get the img from the details pane
    var image = document.getElementById("image");

    document.getElementById("category").innerText = category + " - " + time

    if(description != ""){
        document.getElementById("description_title").style.visibility = "visible";
    }else{
        document.getElementById("description_title").style.visibility = "hidden";
    }

    document.getElementById("description").innerText = description

    image.src = url
}

function closeDetails() {
    // Close the Side Window
    document.getElementById("sideDetails").style.width = "0";
}

function openNewReport() {
    if(newMarker != null){
        newMarker.setMap(null)
    }

    // Open the Side Window
    document.getElementById("sideDetails").style.width = "630px";

    newMarker = new google.maps.Marker({
        position: mapInstance.getCenter(),
        draggable: true
    });

    newMarker.setMap(mapInstance)
}

function closeNewReport() {
    // Hide the new Marker
    if(newMarker != null){
        newMarker.setMap(null)
    }

    // Close the Side Window
    document.getElementById("sideDetails").style.width = "0";
}