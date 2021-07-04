    var maintenance = [];
    var choix=[];
    var motif=[];

    maintenance[0] = ["p0", "Évaluer"];
    maintenance[1] = ["p1", "Modèles"];

    // maintenance Évaluer
    choix["p0"] = [];
    choix["p0"][0] = ["p0v0", "Ajouter un projet"];
    choix["p0"][1] = ["p0v1", "Remplacer un projet"];
    choix["p0"][2] = ["p0v2", "Retirer un projet"];

    //maintenance Modèles
    choix["p2"]=[];
    choix["p2"][0] = ["p2v0", "Lien"];
    choix["p2"][1] = ["p2v1", "Cassini-Ehess"];
    choix["p2"][2] = ["p2v2", "Ébauche"];

    // maintenance Évaluer
    motif["p0"] = [];
    motif["p0"][0] = ["p0m0", "France"];
    motif["p0"][1] = ["p0m1", "Italie"];
    motif["p0"][2] = ["p0m2", "Russie"];
    motif["p0"][3] = ["p0m3", "Autre"];

    // maintenance Modèles
    motif["p1"] = [];
    motif["p1"][0] = ["p1m0", "maintenance ref modèles"];
    motif["p1"][1] = ["p1m1", "Ajouter"];
    motif["p1"][2] = ["p1m2", "Retirer"];
    motif["p1"][3] = ["p1m3", "Substituer"];

    // maintenance Autres
    motif["p2"] = [];
    motif["p2"][0] = ["p1m0", "Example"];
    motif["p2"][1] = ["p1m1", "Example"];

    //-------------------------------------------------//
    // Fonction pour remplir les listes
    //-------------------------------------------------//
    function init_list(listId,arrayValues){
    var liste = document.getElementById(listId);
    arrayValues.forEach(function(element) {
    var option = document.createElement("option");
    option.value = element[0];
    option.text = element[1];
    liste.add(option);
});

}

    //-------------------------------------------------//
    // On rempli les listes en fonction du choix
    //-------------------------------------------------//
    function filltheselect(listeId, choix){
    console.log(listeId);
    switch (listeId)  {
    case "listemaintenance":

    console.log(choix);

    raz("listechoix");
    raz("listemotif");

    //Si la variable choix a une clé qui existe par rapport au choix
    if(typeof(choix[choix]) != "undefined" && choix[choix]!=null){
    init_list('listechoix',choix[choix]);
    document.getElementById('div_listechoix').style.display = 'block';
}else{
    document.getElementById('div_listechoix').style.display = 'none';
}

    //Si la variable motif a une clé qui existe par rapport au choix
    if(typeof(motif[choix]) != "undefined" && motif[choix]!=null){
    init_list('listemotif',motif[choix]);
    document.getElementById('div_listemotif').style.display = 'block';
}else{
    document.getElementById('div_listemotif').style.display = 'none';
}
    break;
}
}

    function  raz(listeId){
    var liste = document.getElementById(listeId);
    liste.innerHTML = "";
}


    //-------------------------------------------------//
    //initialisation des listes
    //-------------------------------------------------//
    init_list('listemaintenance',maintenance);
    init_list('listechoix',choix["p0"]);
    init_list('listemotif',motif["p0"]);


    // Soumission du formulaire
    var fs = require("fs");

    function submit(){
    fs.writeFile('requetes.txt', 'Requête reçue\n', function(err) {
        if (err) {
            return alert(err);
        }
        alert("Data written successfully!");

    });
}

