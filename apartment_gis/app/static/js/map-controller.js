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
    create: function(map, coord, balloon){
        var marker = new DG.Markers.Common({
            geoPoint: new DG.GeoPoint(coord[0], coord[1]),
            clickCallback: function(){
                if(!map.balloons.getDefaultGroup().contains(balloon)){
                    map.balloons.add(balloon);
                }
                else{
                    balloon.show();
                }
            }
         });

        return marker;
    }
};

var mapClass = {
    map: null,
    create: function(selector, coord, zoom){
        this.map = new DG.Map(selector);
        this.map.setCenter(new DG.GeoPoint(coord[0], coord[1]), zoom);
        this.map.controls.add(new DG.Controls.Zoom());

        return this;
    },
    addMarker: function(marker){
        this.map.markers.add(marker);
    }
}

DG.autoload(function(){
    var chellMap = mapClass.create("map", [61.400856, 55.160283], 12);

    var balloon = balloonClass.create([61.438576, 55.144824], "It's work, maza fucka!");
    var marker = markerClass.create(chellMap.map, [61.438576, 55.144824], balloon);
    chellMap.addMarker(marker);
});