window.addEventListener('DOMContentLoaded', () => {

    const newpostModal = document.getElementById('newpost')
    newpostModal.addEventListener('shown.bs.modal', event => {
        console.log(event.target)
        const saveBtn = newpostModal.querySelector('#savepost')
        saveBtn.onclick = async function (e) {
            const title = newpostModal.querySelector('#newtitle').value
            const content = newpostModal.querySelector('#newcontent').value
            const paragraphs = content.split(/\n{2,}/).map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`);
            const newContent = `<div>${paragraphs.join('')}</div>`;

            const post = {
                "title": title,
                "content": newContent
            }
            await newPost(post)
            window.location.reload();
        }
    })

    const upModal = document.getElementById('updatepost')
    upModal.addEventListener('shown.bs.modal', (event) => {
        let uuid = event.relatedTarget.getAttribute('data-id')
        getPost(uuid).then(post => {
            console.log(post);
            upModal.querySelector('#uptitle').value = post.title
            const text = post.content.replace(/<br>/g, '\n').replace(/<[^>]*>/g, '');
            upModal.querySelector('#upcontent').value = text;
            upModal.querySelector('#createdDate').innerHTML = post.dt_created
        })
        const saveBtn = upModal.querySelector('#savepost')
        saveBtn.onclick = async function (e) {
            const title = upModal.querySelector('#uptitle').value
            const content = upModal.querySelector('#upcontent').value
            const paragraphs = content.replace(/\n/g, '<br>');
            const newContent = `<p>${paragraphs}</p>`;
            const dt_created = upModal.querySelector('#createdDate').innerHTML

            const post = {
                "id": uuid,
                "title": title,
                "content": newContent,
                "dt_created": dt_created
            }
            await updatePost(post)
            window.location.reload();
        }

    })

    const delModal = document.getElementById('deletepost')
    delModal.addEventListener('shown.bs.modal', (event) => {
        let uuid = event.relatedTarget.getAttribute('data-id')
        const delBtn = delModal.querySelector('#deletepost')
        delBtn.onclick = function (e) {
            delete_post(uuid).then(post => {
                window.location.reload();
            })

        }

    })

});

async function getPost(id) {
    try {
        const response = await fetch('/get_post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "id": id })
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function delete_post(id) {
    try {
        const response = await fetch('/delete_post/' + id, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
        });

        const data = await response.json();
        return JSON.parse(data.post);
    } catch (error) {
        console.error('Error:', error);
    }

}

async function newPost(post) {
    try {
        const response = await fetch('/new_post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(post)
        });

        const data = await response.json();
        return JSON.parse(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function updatePost(post) {
    try {
        const response = await fetch('/update_post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(post)
        });

        const data = await response.json();
        return JSON.parse(data);
    } catch (error) {
        console.error('Error:', error);
    }
}