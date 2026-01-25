// 全局变量
const API_BASE = 'https://api.github.com';

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 设置默认日期为今天
    document.getElementById('publishDate').valueAsDate = new Date();

    // 监听图片URL变化，显示预览
    document.getElementById('imageUrl').addEventListener('input', updatePreview);

    // 表单提交
    document.getElementById('articleForm').addEventListener('submit', handleSubmit);
});

// 图片上传到SM.MS图床
async function uploadImage() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';

    input.onchange = async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        showMessage('正在上传图片...', 'info');

        try {
            const formData = new FormData();
            formData.append('smfile', file);

            const response = await fetch('https://sm.ms/api/v2/upload', {
                method: 'POST',
                headers: {
                    'Authorization': CONFIG.imageHostToken || ''
                },
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById('imageUrl').value = result.data.url;
                showMessage('图片上传成功！', 'success');
                updatePreview();
            } else {
                throw new Error(result.message || '上传失败');
            }
        } catch (error) {
            console.error('上传错误:', error);
            showMessage('图片上传失败：' + error.message, 'error');
        }
    };

    input.click();
}

// 更新预览
function updatePreview() {
    const imageUrl = document.getElementById('imageUrl').value;
    const title = document.getElementById('title').value;
    const date = document.getElementById('publishDate').value;

    if (imageUrl) {
        const previewSection = document.getElementById('previewSection');
        if (previewSection) {
            previewSection.classList.add('show');
            const previewImage = document.getElementById('previewImage');
            if (previewImage) {
                // 获取第一行URL作为预览图
                const firstImageUrl = imageUrl.split('\n')[0].trim();
                previewImage.src = firstImageUrl;
            }
            const previewTitle = document.getElementById('previewTitle');
            if (previewTitle) {
                previewTitle.textContent = title || '未填写标题';
            }
            const previewDate = document.getElementById('previewDate');
            if (previewDate) {
                previewDate.textContent = date || '未选择日期';
            }
        }
    } else {
        const previewSection = document.getElementById('previewSection');
        if (previewSection) {
            previewSection.classList.remove('show');
        }
    }
}

// 表单提交处理
async function handleSubmit(e) {
    e.preventDefault();

    // 验证配置
    if (!validateConfig()) {
        return;
    }

    // 收集表单数据
    // 处理多个图片URL
    const imageUrlText = document.getElementById('imageUrl').value;
    const imageUrls = imageUrlText.split('\n')
        .map(url => url.trim())
        .filter(url => url.length > 0);

    if (imageUrls.length === 0) {
        showMessage('请至少填写一个图片URL', 'error');
        return;
    }

    const article = {
        id: generateArticleId(),
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        imageUrl: imageUrls[0], // 第一张图作为主图
        imageUrls: imageUrls, // 所有图片URL数组
        thumbnailUrl: imageUrls[0], // 使用第一张图作为缩略图
        tags: [], // 空数组
        category: '', // 空字符串
        publishDate: document.getElementById('publishDate').value,
        videoId: document.getElementById('videoId').value,
        author: document.getElementById('author').value,
        viewCount: 0,
        downloadCount: 0,
        favoriteCount: 0
    };

    // 显示加载状态
    document.getElementById('loading').classList.add('show');
    document.querySelector('.btn[type="submit"]').disabled = true;

    try {
        // 获取现有数据
        const currentData = await fetchCurrentData();

        // 添加新文章
        currentData.articles.unshift(article); // 新文章放在最前面
        currentData.meta.totalCount = currentData.articles.length;
        currentData.meta.lastUpdate = new Date().toISOString().split('T')[0];

        // 提交到GitHub
        await commitToGitHub(currentData);

        showMessage('文章发布成功！已同步到GitHub', 'success');

        // 重置表单
        document.getElementById('articleForm').reset();
        document.getElementById('publishDate').valueAsDate = new Date();
        const previewSection = document.getElementById('previewSection');
        if (previewSection) {
            previewSection.classList.remove('show');
        }

        // 3秒后清除消息
        setTimeout(() => {
            hideMessage();
        }, 3000);

    } catch (error) {
        console.error('提交错误:', error);
        showMessage('发布失败：' + error.message, 'error');
    } finally {
        document.getElementById('loading').classList.remove('show');
        document.querySelector('.btn[type="submit"]').disabled = false;
    }
}

// 生成文章ID
function generateArticleId() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    // 获取现有文章数量作为序号
    return `${year}${month}${day}${String(Math.floor(Math.random() * 999)).padStart(3, '0')}`;
}

// 获取当前数据
async function fetchCurrentData() {
    const url = `${API_BASE}/repos/${CONFIG.githubOwner}/${CONFIG.githubRepo}/contents/${CONFIG.dataFilePath}?ref=${CONFIG.branch}`;

    const response = await fetch(url, {
        headers: {
            'Authorization': `token ${CONFIG.githubToken}`,
            'Accept': 'application/vnd.github.v3+json'
        }
    });

    if (!response.ok) {
        throw new Error('获取数据失败，请检查配置和网络连接');
    }

    const result = await response.json();

    // 正确解码Base64（支持UTF-8中文）
    const binaryString = atob(result.content.replace(/\n/g, ''));
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    const decoder = new TextDecoder();
    const content = decoder.decode(bytes);

    return JSON.parse(content);
}

// 提交到GitHub
async function commitToGitHub(data) {
    const url = `${API_BASE}/repos/${CONFIG.githubOwner}/${CONFIG.githubRepo}/contents/${CONFIG.dataFilePath}`;

    // 获取文件的SHA（更新文件需要）
    const currentFile = await fetch(url + `?ref=${CONFIG.branch}`, {
        headers: {
            'Authorization': `token ${CONFIG.githubToken}`,
            'Accept': 'application/vnd.github.v3+json'
        }
    });

    const currentFileData = await currentFile.json();
    const sha = currentFileData.sha;

    // 将数据转为Base64（支持中文）
    const jsonStr = JSON.stringify(data, null, 2);
    const encoder = new TextEncoder();
    const dataUint8 = encoder.encode(jsonStr);
    let binary = '';
    dataUint8.forEach(byte => {
        binary += String.fromCharCode(byte);
    });
    const content = btoa(binary);

    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Authorization': `token ${CONFIG.githubToken}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: `更新文章数据 - ${new Date().toLocaleString('zh-CN')}`,
            content: content,
            sha: sha,
            branch: CONFIG.branch
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || '提交到GitHub失败');
    }

    return await response.json();
}

// 显示消息
function showMessage(text, type = 'success') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = text;
    messageEl.className = `message show ${type}`;
}

function hideMessage() {
    const messageEl = document.getElementById('message');
    messageEl.classList.remove('show');
}
