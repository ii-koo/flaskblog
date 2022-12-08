function editAccount(id){
    const form = document.getElementById(id);

    if(form.classList.contains('d-none')){
        form.classList.remove('d-none');
    }else{
        form.classList.add('d-none');
    }
}