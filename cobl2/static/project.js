CLLD.MapIcons.div = function(feature, size, url) {
        return L.divIcon({
            html: '<div class="gl-map-icon" style="background: #' + feature.properties.language.color + ';">☺</div>',
            className: 'clld-map-icon'
        });
};


