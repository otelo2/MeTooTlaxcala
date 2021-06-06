const search = document.getElementById('search');
const matchList = document.getElementById('match-list');
const accent_map = {'á':'a', 'é':'e', 'í':'i','ó':'o','ú':'u'};

//Searchs for the abusers in the abusador.json and filters them
const searchAbusers = async searchText => {
    const res = await fetch('../data/abusador.json');
    const abusers = await res.json();

    //Get matches to current text input
    let matches = abusers.filter(abuser => {
        const regex = new RegExp(`^${accent_fold(searchText)}`, 'gi');
        //Replace NULL's with nothing. This isn't good, but idc
        if(abuser.nombre=="NULL"){
            abuser.nombre=""
        }
        if(abuser.apellidopaterno=="NULL"){
            abuser.apellidopaterno=""
        }
        if(abuser.apellidomaterno=="NULL"){
            abuser.apellidomaterno=""
        }
        if(abuser.imagen1=="NULL"){
            abuser.imagen1=""
        }
        if(abuser.imagen2=="NULL"){
            abuser.imagen2=""
        }
        if(abuser.imagen3=="NULL"){
            abuser.imagen3=""
        }
        if(abuser.imagen4=="NULL"){
            abuser.imagen4=""
        }

        //Remove special symbols (#) in image path
        if(abuser.imagen1.includes("#")){
            abuser.imagen1 = abuser.imagen1.replaceAll("#", "%23")
        }
        if(abuser.imagen2.includes("#")){
            abuser.imagen2 = abuser.imagen2.replaceAll("#", "%23")
        }
        if(abuser.imagen3.includes("#")){
            abuser.imagen3 = abuser.imagen3.replaceAll("#", "%23")
        }
        if(abuser.imagen4.includes("#")){
            abuser.imagen4 = abuser.imagen4.replaceAll("#", "%23")
        }

        //Accent folding
        abuser.nombre = accent_fold(abuser.nombre)
        abuser.apellidopaterno = accent_fold(abuser.apellidopaterno)
        abuser.apellidomaterno = accent_fold(abuser.apellidomaterno)

        //Get first and second name, if any
        nombres = abuser.nombre.split(" ")
        primerNombre = nombres[0]
        segundoNombre = nombres[1]
        
        if (segundoNombre === undefined) {
            return primerNombre.match(regex) || abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
        }
        if (primerNombre === undefined) {
            return  segundoNombre.match(regex) || abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
        }
        if (primerNombre === undefined && segundoNombre === undefined) {
            return abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
        }
        else {
            return primerNombre.match(regex) || segundoNombre.match(regex) || abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
        }
    });

    

    if(matches.length === 0) {
        matchList.innerHTML = '<p class="text-warning">No se encontraron coincidencias para tu búsqueda</p>'
    }

    if(searchText.length === 0) {
        matches = [];
        matchList.innerHTML = ''
    }

    outputHtml(matches);
}

//Show results in HTML
const outputHtml = matches => {
    if(matches.length > 0) {
        const html = matches.map(match => `
            <div class="card card-body mb-1">
                <h4><span class="text-primary">${match.nombre}</span> ${match.apellidopaterno} ${match.apellidomaterno} </h4>
                <h6 class="card-subtitle mb-2 text-muted">${match.denuncia}</h6>
                <img src="../${match.imagen1}" alt="${match.imagen1}"></img>
                <img src="../${match.imagen2}" alt="${match.imagen2}"></img>
                <img src="../${match.imagen3}" alt="${match.imagen3}"></img>
                <img src="../${match.imagen4}" alt="${match.imagen4}"></img>
                <small>${match.fecha}  ${match.hora}</small>
                <a href="${match.link}">${match.link}</a>
            </div>
        `
        ).join('');

        matchList.innerHTML = html;
    }
}

search.addEventListener('input', () => searchAbusers(search.value));

function accent_fold (s) {
    if (!s) { return ''; }
    var ret = '';
    for (var i = 0; i < s.length; i++) {
        ret += accent_map[s.charAt(i)] || s.charAt(i);
    }
    return ret;
};