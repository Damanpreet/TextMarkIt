// Function to change the background color of text to green.
function highlightBackground(click_id){
    var elem = document.getElementById(click_id); // retrieve the element from the click id.
    elem.style.backgroundColor="#00ff00"; // highlight the background of this element.
    
    // expand this element.
    if (elem.style.maxHeight){
        elem.previousElementSibling.value = "-";
        elem.style.maxHeight = null;        
    }
}

// Function to remove the "green" background color.
function removeBackground(click_id){
    var elem = document.getElementById(click_id);
    elem.style.removeProperty("background-color");
    
    // collapse this element.
    if (!elem.style.maxHeight){
        elem.previousElementSibling.value = "+";
        elem.style.maxHeight = 1 + "px";
    }
}

// Function to find similarity on favortize and de-favoritizing a text.
function reply_click(click_id, pageno){
    if (document.getElementById(click_id).style.backgroundColor==="rgb(0, 255, 0)"){
        removeBackground(click_id);

        // de-favoritize the paragraphs linked to this paragraph.
        document.getElementById("blink").style.display="inline";
        
        $.ajax({
            url: "/api/delete_similarity",
            type: "post",
            data: {pageno: pageno, para_id: click_id.split("-")[1]},
            success: function(response){
                // check if the response is an array.
                if ($.isArray(response) && response.length){
                    console.log(response);
                    response.forEach(removeBackground);
                    console.log("De-favoritized similar text.");
                }
            },
            error: function(response){
                console.log('Error while de-favoritizing similar text in the document.');
            }
        })
        document.getElementById("blink").style.display="none";

    }
    else{ // favoritize all the paragraphs linked to the current paragraph.
        document.getElementById("blink").style.display="inline";
        
        $.ajax({
            url: "/api/similarity",
            type: "post",
            data: {pageno: pageno, para_id: click_id.split("-")[1]},
            success: function(response){
                console.log(response);
                // check if the response is an array
                if ($.isArray(response) && response.length){
                    response.forEach(highlightBackground);
                    console.log("Highlighted similar text.");
                }
                highlightBackground(click_id);
            },
            error: function(response){
                console.log('Error while highlighting similar text in the document.');
            }
        })
        document.getElementById("blink").style.display="none";
    }
}

// function for the collapse button
function collapse_elem(click_id){
    elem = document.getElementById(click_id);
    elem.classList.toggle("active");
    
    var content = elem.nextElementSibling; // this returns the button.
    if (content.style.maxHeight){
        content.style.maxHeight = null;
        elem.value = "-";
    }
    else{
        elem.value = "+";
        content.style.maxHeight = 1 + "px";
    }
}

// Load suggestions 
function loadSuggestions(identifier, pageno){
    if(identifier=='next')
    {
        // display "loading suggestions" message.
        document.getElementById("blink").style.display="inline";
        
        // load new suggestions, if next is clicked.
        // compute similarity on the new page based on previously favoritized paragraphs.
        $.ajax({
            url: "/api/load_suggestions",
            type: "post", 
            data: {"pageno": pageno, "identifier": identifier},
            success: function(response){
                console.log("updated next page. Page no: ", pageno);
                console.log(response);
                console.log("**************");
                if ($.isArray(response) && response.length){
                    response.forEach(highlightBackground);
                }

                // toggle all the elements which are not in the list of favorites.
                for (var i=1; i<=100; i++){
                    if (!response.includes('button-'+i)){         
                        // check if the element exists.           
                        if (document.getElementById('collapse-'+i)!=null){
                            collapse_elem('collapse-'+i); 
                        }
                    }
                }

                document.getElementById("blink").style.display="none"; // turn off the message after similarities are loaded.
            },
            error: function(response){
                console.log('Error while loading next suggestions for similar text on the current page.');
            }
        });
    }
    else if(identifier=='prev')
    {
        // display "loading suggestions" message.
        document.getElementById("blink").style.display="inline";
        
        // use the previously loaded suggestions.
        // send a request to find the paragraphs to be highlighted.
        $.ajax({
            url: "/api/load_suggestions",
            type: "post", 
            data: {"pageno": pageno, "identifier": identifier},
            success: function(response){
                console.log("updated prev page. Page no: ", pageno);
                console.log(response);
                console.log("**************");
                if ($.isArray(response) && response.length){
                    response.forEach(highlightBackground);
                }
                debugger;
                // toggle all the elements which are not in the list of favorites.
                for (var i=1; i<=100; i++){
                    if (!response.includes('button-'+i)){         
                        // check if the element exists.           
                        if (document.getElementById('collapse-'+i)!=null){
                            collapse_elem('collapse-'+i); 
                        }
                    }
                }

                // turn off the message after similarities are loaded.
                document.getElementById("blink").style.display="none"; 
            },
            error: function(response){
                console.log('Error while loading previous suggestions for similar text on the current page.');
            }
        });      
    }
}
