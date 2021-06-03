const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

//Searchs for the abusers in the abusador.json and filters them
const searchAbusers = async searchText => {
    const res = await fetch('../Frontend/data/abusador.json');
    const abusers = await res.json();

    //Get matches to current text input
    let matches = abusers.filter(abuser => {
        const regex = new RegExp(`^${searchText}`, 'gi');
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
            abuser.imagen1 = abuser.imagen1.replace("#", "%23")
        }
        if(abuser.imagen2.includes("#")){
            abuser.imagen2 = abuser.imagen2.replace("#", "%23")
        }
        if(abuser.imagen3.includes("#")){
            abuser.imagen3 = abuser.imagen3.replace("#", "%23")
        }
        if(abuser.imagen4.includes("#")){
            abuser.imagen4 = abuser.imagen4.replace("#", "%23")
        }

        return abuser.nombre.match(regex) || abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
    });

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
                <small>${match.denuncia}</small>
                <img src="../Frontend${match.imagen1}" alt="${match.imagen1}"></img>
                <img src="../Frontend${match.imagen2}" alt="${match.imagen2}"></img>
                <img src="../Frontend${match.imagen3}" alt="${match.imagen3}"></img>
                <img src="../Frontend${match.imagen4}" alt="${match.imagen4}"></img>
                <small>${match.fecha}  ${match.hora}</small>
                <a href="${match.link}">${match.link}</a>
            </div>
        `
        ).join('');

        matchList.innerHTML = html;
    }
}

search.addEventListener('input', () => searchAbusers(search.value));