// Scripts liés à la page list_riddles.html
// Mise à jour du niveau de difficulté :
$('.level_down_up').click(function(e) {
    e.preventDefault();
    var $button =$(this);
    var url = $button.attr('href');
    //alert(url);
    $.ajax({
        url: url,
        success: function(new_value) {
            document.getElementById("debug").innerHTML +="Level : "+new_value;
            $button.parent().find('.level').text(new_value);
        }
    });
});
//Affichage de la réponse :
$(".show_answer").click(function() {
    var $button=$(this);
    if ($button.text() == "Afficher la réponse") {
        $button.text("Cacher la réponse");
        $button.parent().find(".answer").show();
    } else {
        $button.text("Afficher la réponse");
        $button.parent().find(".answer").hide();
    }
});

// Suppression d'énigmes
$('.delete_riddle').click(function(e) {
    e.preventDefault();
    var $button=$(this);
    var url = $button.attr('href');

    $.ajax({
        url: url,
        success : function (result) {  // attendu dans 'data', une liste de json.
            data = result.riddles;
            //document.getElementById("debug").innerHTML +="Result : "+result.per_page;
            for (i in data) {
                var riddleid = $("#riddlediv_"+i).find(".riddleid").text();

                //On passe les indices présent dans la page au même index dans le même ordre que ceux dans le JSON
                if (riddleid == data[i].id) {
                    continue;
                }

                //document.getElementById("debug").innerHTML +="Data : "+i+";Clues length :"+data[i].clues.length;
                // on adapte les réponses et les niveaux
                $("#riddlediv_"+i).find(".riddle").html("<b>Enigme : </b>"+data[i].riddle);
                $("#riddlediv_"+i).find(".answer").text(data[i].answer);
                $("#riddlediv_"+i).find(".level").text(data[i].level);

                // On adapte les url
                $("#riddlediv_"+i+" .riddle_id").each(function() {
                        var url = $(this).attr('href');
                        var new_target = "riddle_id="+data[i].id;
                        url=url.replace(/riddle_id=([0-9]+)/,new_target);
                        //document.getElementById("debug").innerHTML += 'url:'+url+"</br>\n";
                        $(this).attr("href",url);
                });
                // On adpate la liste des indices :
                // 1. En effaçant la liste des indices s'il existent pour l'énigme courante :
                //$("#riddlediv_"+i).find(".clue_next").css("background-color","blue").html("Je t'ai trouvé !");
                // 1. En supprimant les indices pour l'ancienne énigme
                $("#riddlediv_"+i).find(".clues .list-group").remove();

                // 2. En recréant la liste des indices pour la nouvelle énigme s'il y en a :
                var clue_html="";
                var clue_list="";
                var clue_add="";

                if (data[i].clues.length > 0) {
                  //document.getElementById("debug").innerHTML +="Data : "+i+";Clues length :"+data[i].clues.length;
                  clue_html=`<ul class="list-group">\n`;
                    var clue_num=0;
                    for (clue in data[i].clues) {
                        clue_list +=
                            `<li class="list-group-item">\n
                             \t ${data[i].clues[clue_num].clue}
                             \t <a href="/delete_clue?riddle_id=${data[i].id}&clue_id=${data[i].clues[clue_num].id}">
                                    <button type="button" class="btn btn-outline-danger btn-sm" style="float:right">Supprimer</button></a>\n
                             \t <a href="/update_clue?riddle_id=${data[i].id}&clue_id=${data[i].clues[clue_num].id}">
                                    <button type="button" class="btn btn-outline-primary btn-sm" style="float:right">Modifier</button></a>\n
                             </li>\n
                            `;
                        clue_num++;
                    }
                    clue_html=clue_html+clue_list+"</ul></div>";
                    $("#riddlediv_"+i).find(".clue_list").html(clue_html);
                }
            }
            // Supprimer les énigmes superflues  dans la page (quand le nombre de JSON dans data < nombre d'énigmes affichées)
            var dom_count = $(".riddlediv").length;
            var json_count = data.length;
            while (dom_count > json_count) {
                //document.getElementById("debug").innerHTML += "DomCount:"+dom_count+";JsonCount :"+json_count+"</br>\n";
                $("#riddlediv_"+(dom_count-1)).remove();
                dom_count--;
            }
        }
    });
});
// Suppression d'indices
$('.delete_clue').click(function(e) {
    e.preventDefault();
    var $button = $(this);
    var url = $button.attr('href');
    $.ajax({
        url: url,
        success: function (data) {
            //alert('bonjour:'+url);
            $button.parent().remove();
        }
    });
});
