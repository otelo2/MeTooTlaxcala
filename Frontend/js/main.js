const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

//Searchs for the abusers in the abusador.json and filters them
const searchAbusers = async searchText => {
    const res = await fetch('../Frontend/data/abusador.json');
    const abusers = await res.json();

    //Get matches to current text input
    let matches = abusers.filter(abuser => {
        const regex = new RegExp(`^${searchText}`, 'gi');
        return abuser.nombre.match(regex) || abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
    });

    //We are at 12:51 https://www.youtube.com/watch?v=1iysNUrI3lw
    console.log(matches);
}

search.addEventListener('input', () => searchAbusers(search.value));