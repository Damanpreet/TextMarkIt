function reply_click(click_id){
    // alert(document.getElementById(click_id));
    if (document.getElementById(click_id).style.backgroundColor==="rgb(0, 255, 0)"){
        document.getElementById(click_id).style.removeProperty("background-color");
    }
    else{
        document.getElementById(click_id).style.backgroundColor="#00ff00";
    }
}

function collapse_elem(click_id){
    elem = document.getElementById(click_id)
    elem.classList.toggle("active");
    var content = elem.nextElementSibling;
    if (content.style.maxHeight){
        content.style.maxHeight = null;
        elem.value = "-";
    }
    else{
        elem.value = "+";
        content.style.maxHeight = 1 + "px";
    }
}

function loadnextpage(pageno){
    $.ajax({
        url: "/api/paginate",
        type: "post",
        data: {pageno: pageno},
        // , prevresult: prevresult, currresult: currresult},
        success: function(response){
            console.log('Successfully loaded the next page!');
            // window.location.replace('/api/paginate');
            console.log(response);
            document.write(response);
        },
        error: function(response){
            console.log('Error loading the next page!');
            // window.location.replace('/api/paginate');
        }
    })
}