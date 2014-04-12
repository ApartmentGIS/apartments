var balloonClass = {
    create: function(coords, text){
        var balloon = new DG.Balloons.Common({
            geoPoint: new DG.GeoPoint(coords[0], coords[1]),
            contentHtml: text
        });

        return balloon;
    }
};

var markerClass = {
    create: function(map, selectedBaloonsGroupName, coord, balloon, selectedText, callback){
        var marker = new DG.Markers.Common({
            geoPoint: new DG.GeoPoint(coord[0], coord[1]),
            clickCallback: function(){
                var tempBalloon = balloonClass.create(coord, selectedText),
                    selectedBalloonsGroup = map.balloons.getGroup(selectedBaloonsGroupName);

                selectedBalloonsGroup.removeAll();
                selectedBalloonsGroup.add(tempBalloon);
                tempBalloon.show();

                callback(balloon.getContent());
            }
         });

        return marker;
    }
};

var mapClass = {
    map: null,
    selectedBalloonsGroupName: null,
    create: function(selector, selectedBalloonsGroupName, coord, currentZoom, minZoom){
        this.map = new DG.Map(selector);
        this.map.setCenter(new DG.GeoPoint(coord[0], coord[1]), currentZoom);
        this.map.setMinZoom(minZoom);
        this.map.controls.add(new DG.Controls.Zoom());

        this.selectedBalloonsGroupName = selectedBalloonsGroupName;
        this.map.balloons.createGroup(selectedBalloonsGroupName);

        return this;
    },
    addMarkers: function(markers){
        for(var i = 0; i < markers.length; i++){
            this.map.markers.add(markers[i]);
        }
    }
};