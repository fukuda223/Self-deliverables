$(document).ready(function() {
    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d');
    const colorPicker = document.getElementById('color-picker');
    const lineWidthSlider = document.getElementById('line-width');
    const clearButton = document.getElementById('clear-button');
    const saveButton = document.getElementById('save-button');
    const threadsContainer = $('#threads-container');
    const rankingContainer = $('#ranking-container');
    const socket = io();

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    let currentThreadId = null;

    // 初期設定
    ctx.lineWidth = lineWidthSlider.value;
    ctx.lineCap = 'round';
    ctx.strokeStyle = colorPicker.value;

    // 描画イベントリスナー
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });

    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseout', () => isDrawing = false);

    function draw(e) {
        if (!isDrawing) return;
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    // ツール操作
    colorPicker.addEventListener('change', () => {
        ctx.strokeStyle = colorPicker.value;
    });

    lineWidthSlider.addEventListener('change', () => {
        ctx.lineWidth = lineWidthSlider.value;
    });

    clearButton.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    // スレッド作成フォーム
    $('#new-thread-form').on('submit', function(e) {
        e.preventDefault();
        const title = $('#thread-title').val();
        if (title.trim() === '') return;

        $.ajax({
            url: '/create_thread',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ title: title }),
            success: function(response) {
                if (response.success) {
                    $('#thread-title').val('');
                    displayThread(response.thread);
                }
            }
        });
    });

    // 画像保存
    saveButton.addEventListener('click', () => {
        if (currentThreadId === null) {
            alert('投稿するスレッドを選択してください。');
            return;
        }

        const imageData = canvas.toDataURL('image/png');
        
        $.ajax({
            url: '/upload_drawing',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                image_data: imageData,
                thread_id: currentThreadId
            }),
            success: function(response) {
                if (response.success) {
                    alert('絵が投稿されました！');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
            }
        });
    });

    // スレッド表示
    function displayThread(thread) {
        const threadItem = $(`
            <div class="thread-item" data-id="${thread.id}">
                <h3>${thread.title}</h3>
                <div class="drawings-list"></div>
            </div>
        `);
        threadsContainer.append(threadItem);

        // スレッドクリックで描画エリアのタイトルを更新
        threadItem.on('click', function() {
            currentThreadId = $(this).data('id');
            $('#drawing-area h2').text(`お絵かきスペース：${thread.title}`);
        });

        // 既存の絵を表示
        if (thread.drawings && thread.drawings.length > 0) {
            thread.drawings.forEach(drawing => displayDrawing(drawing, threadItem.find('.drawings-list')));
        }
    }

    // 絵の表示
    function displayDrawing(drawing, container) {
        const drawingItem = $(`
            <div class="drawing-item" data-id="${drawing.id}">
                <img src="${drawing.image_url}" class="drawing-image">
                <div class="drawing-meta">
                    <button class="like-button" data-id="${drawing.id}">❤️</button>
                    <span class="like-count">${drawing.likes}</span>
                </div>
            </div>
        `);
        container.append(drawingItem);

        drawingItem.find('.like-button').on('click', function() {
            const drawingId = $(this).data('id');
            $.ajax({
                url: '/like_drawing',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ drawing_id: drawingId }),
                success: function(response) {
                    if (response.success) {
                        // サーバーから更新されたいいね数を受け取るので、ここでは何もしない
                    }
                }
            });
        });
    }

    // ランキング表示
    function displayRanking(ranking) {
        rankingContainer.empty();
        ranking.forEach((drawing, index) => {
            const rankingItem = $(`
                <div class="ranking-item">
                    <h4>${index + 1}位</h4>
                    <img src="${drawing.image_url}" class="drawing-image">
                    <p>いいね数: ${drawing.likes}</p>
                </div>
            `);
            rankingContainer.append(rankingItem);
        });
    }

    // Socket.IOからのイベント処理
    socket.on('initial_data', (data) => {
        console.log('Initial data received:', data);
        data.threads.forEach(thread => displayThread(thread));
        displayRanking(data.ranking);
    });

    socket.on('new_drawing_posted', (drawing) => {
        console.log('New drawing posted:', drawing);
        const threadContainer = threadsContainer.find(`.thread-item[data-id="${drawing.thread_id}"] .drawings-list`);
        displayDrawing(drawing, threadContainer);
    });

    socket.on('update_like_count', (data) => {
        const likeCountSpan = $(`[data-id="${data.id}"] .like-count`);
        if (likeCountSpan) {
            likeCountSpan.text(data.likes);
        }
    });

    socket.on('update_ranking', (ranking) => {
        console.log('Ranking updated:', ranking);
        displayRanking(ranking);
    });

});