function markFixed(id) {
    fetch(`/fix/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => {
        if (res.ok) {
            location.reload();
        } else {
            alert("Failed to mark as fixed.");
        }
    });
}

function confirmDelete(id) {
    if (confirm("Are you sure you want to delete this detection?")) {
        fetch(`/delete/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => {
            if (res.ok) {
                location.reload();
            } else {
                alert("Failed to delete.");
            }
        });
    }
}
