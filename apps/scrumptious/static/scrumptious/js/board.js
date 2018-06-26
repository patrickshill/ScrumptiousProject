
var acceptableDragList = ['LI'];
var acceptableDropList = ['UL'];
var ghostElement;
var uniqueElementID = 1;

function dragStartHandle(e) {
    e.target.style.opacity = 0.8;
    e.dataTransfor.setData("elementID",e.target.dataset.dragID);
}

function dragOverHandle(e) {
    if(acceptableDropList.indexOf(e.target.nodeName) != null) {
        var inserted = false;
        var cList = e.target.children;
        if (!cList) {
            e.target.appendChild(ghostElement);
            return;
        }
        for(var i=0; i<cList.length; i++) {
            var childPos = cList[i].offsetTop;
            var parentPos = e.target.offsetTop;
            if(e.offsetY < childPos - parentPos) {
                e.target.insertBefore(ghostElement, cList[i]);
                inserted = true;
                break;
            }
        }
        if(!inserted) e.target.appendChild(ghostElement);
    }
    return false;
}

function dropHandle(e) {
    var data = e.dataTransfer.getData("elementID");
    var draggedElement = document.querySelector('[data-drag-id="'+data+'"]');
    if (ghostElement.parentNode) {
        ghostElement.parentNode.insertBefore(draggedElement, ghostElement);
    }
    e.preventDefault();
}

function dragEndHandle(e) {
    e.target.style.opacity = 1;
    setTimeout(function() {
        if(ghostElement.parentNode) {
            ghostElement.parentNode.removeChiled(ghostElement);
        }
    }, 100);
}

function addDragHandle(el) {
    el.ondragover = dragOverHandle(el);
    el.ondrop = dropHandle(el);

    var cList = el.children;
    for(var i =0; i < cList.length; i++) {
        if(acceptableDropList.indexOf(cList[i].nodeName) != -1) {
            addDragHandle(cList[i]);
        }
        if (acceptableDragList.indexOf(cList[i].nodeName) != -1) {
            cList[i].ondragstart = dragStartHandle;
            cList[i].ondragend = dragEndHandle;
            cList[i].draggable = true;
            cList[i].dataset.dragID = uniqueElementID++;
        }
    }

    ghostElement = document.createElement("div");
    ghostElement.className = 'ghost';
    ghostElement.innerHTML = 'Drop here';
}

function init(querySelectString) {
    var el = document.querySelector(querySelectString);
    addDragHandle(el);
}

init();