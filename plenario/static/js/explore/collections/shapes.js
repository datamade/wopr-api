var app = app || {};

app.Shapes = Backbone.Collection.extend({
    model: app.Shape,
    url: "http://plenar.io/v1/api/shapes/",
    parse: function(data){
        console.log(data.objects);
        return data.objects;
    }

});