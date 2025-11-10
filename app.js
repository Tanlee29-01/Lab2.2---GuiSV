const API_BASE_URL = 'http://127.0.0.1:5000/api';
const REQUEST_TIMEOUT = 10000;

const elements = {
    searchInput: null,
    addBookButton: null,
    stats: {
        totalBooks: null,
        totalMembers: null,
        borrowingCount: null,
        overdueCount: null
    },
    tables: {
        recentBorrowings: null,
        dueSoon: null,
        books: null,
        members: null
    }
};

document.addEventListener('DOMContentLoaded', () => {
    cacheElements();
    initEventListeners();
    refreshDashboard();
});

function cacheElements() {
    elements.searchInput = document.getElementById('searchInput');
    elements.addBookButton = document.getElementById('addBookBtn');
    elements.addMemberButton = document.getElementById('addMemberBtn');
    elements.borrowButton = document.getElementById('borrowBtn');
    elements.returnButton = document.getElementById('returnBtn');

    elements.stats.totalBooks = document.getElementById('totalBooks');
    elements.stats.totalMembers = document.getElementById('totalMembers');
    elements.stats.borrowingCount = document.getElementById('borrowingCount');
    elements.stats.overdueCount = document.getElementById('overdueCount');

    elements.tables.recentBorrowings = document.getElementById('recentBorrowingsBody');
    elements.tables.dueSoon = document.getElementById('dueSoonBody');
    elements.tables.books = document.getElementById('booksBody');
    elements.tables.members = document.getElementById('membersBody');
}

function initEventListeners() {
    if (elements.searchInput) {
        const debouncedSearch = debounce(() => {
            const keyword = elements.searchInput.value.trim();
            loadBooks(keyword);
        }, 300);
        elements.searchInput.addEventListener('input', debouncedSearch);
    }

    if (elements.addBookButton) {
        elements.addBookButton.addEventListener('click', onAddBookClick);
    }
    if (elements.addMemberButton) {
        elements.addMemberButton.addEventListener('click', onAddMemberClick);
    }
    if (elements.borrowButton) {
        elements.borrowButton.addEventListener('click', onBorrowClick);
    }
    if (elements.returnButton) {
        elements.returnButton.addEventListener('click', onReturnClick);
    }
}

function refreshDashboard() {
    Promise.all([
        loadStats(),
        loadRecentBorrowings(),
        loadUpcomingDueDates(),
        loadBooks(),
        loadMembers()
    ]).catch((error) => {
        console.error('Không thể tải dữ liệu dashboard:', error);
    });
}

async function fetchJSON(path, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    try {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            signal: controller.signal,
            ...options
        });

        if (!response.ok) {
            const contentType = response.headers.get('Content-Type') || '';
            let message = `Request failed with status ${response.status}`;
            try {
                if (contentType.includes('application/json')) {
                    const data = await response.json();
                    message = data?.error || data?.message || JSON.stringify(data);
                } else {
                    const text = await response.text();
                    if (text) {
                        message = text;
                    }
                }
            } catch (parseError) {
                // bỏ qua, dùng message mặc định
            }
            throw new Error(message);
        }

        if (response.status === 204) {
            return null;
        }

        return response.json();
    } finally {
        clearTimeout(timeoutId);
    }
}

async function loadStats() {
    try {
        const stats = await fetchJSON('/stats/overview');
        if (!stats) {
            return;
        }
        updateStatCards(stats);
    } catch (error) {
        console.error('Lỗi khi tải thống kê:', error);
    }
}

function updateStatCards(stats) {
    const mapping = {
        totalBooks: elements.stats.totalBooks,
        totalMembers: elements.stats.totalMembers,
        borrowingCount: elements.stats.borrowingCount,
        overdueCount: elements.stats.overdueCount
    };

    Object.entries(mapping).forEach(([key, node]) => {
        if (node && Object.prototype.hasOwnProperty.call(stats, key)) {
            node.textContent = stats[key];
        }
    });
}

async function loadRecentBorrowings() {
    try {
        const data = await fetchJSON('/borrowings/recent');
        populateTable(elements.tables.recentBorrowings, data, (item) => [
            item.ticketCode ?? '—',
            item.memberName ?? '—',
            item.bookTitle ?? '—',
            formatDate(item.borrowDate)
        ]);
    } catch (error) {
        console.error('Lỗi khi tải sách mượn gần đây:', error);
    }
}

async function loadUpcomingDueDates() {
    try {
        const data = await fetchJSON('/borrowings/due-soon');
        populateTable(elements.tables.dueSoon, data, (item) => [
            item.ticketCode ?? '—',
            item.bookTitle ?? '—',
            item.status ?? '—'
        ]);
    } catch (error) {
        console.error('Lỗi khi tải sách sắp đến hạn:', error);
    }
}

async function loadBooks(keyword = '') {
    try {
        const query = keyword ? `?q=${encodeURIComponent(keyword)}` : '';
        const data = await fetchJSON(`/books${query}`);
        populateTable(elements.tables.books, data, (item) => [
            item.bookId ?? '—',
            item.title ?? '—',
            item.author ?? '—',
            item.category ?? '—',
            item.statusText ?? '—'
        ]);
    } catch (error) {
        console.error('Lỗi khi tải danh sách sách:', error);
    }
}

async function loadMembers() {
    try {
        const data = await fetchJSON('/members');
        populateTable(elements.tables.members, data, (item) => [
            item.memberId ?? '—',
            item.name ?? '—',
            item.email ?? '—',
            item.status ?? '—'
        ]);
    } catch (error) {
        console.error('Lỗi khi tải danh sách thành viên:', error);
    }
}

function populateTable(tbody, data, rowMapper) {
    if (!tbody) {
        return;
    }

    tbody.innerHTML = '';

    const columnCount = tbody.closest('table').querySelectorAll('thead th').length;

    if (!Array.isArray(data) || data.length === 0) {
        const emptyRow = document.createElement('tr');
        const emptyCell = document.createElement('td');
        emptyCell.colSpan = columnCount;
        emptyCell.textContent = 'Không có dữ liệu';
        emptyCell.className = 'empty-cell';
        emptyRow.appendChild(emptyCell);
        tbody.appendChild(emptyRow);
        return;
    }

    data.forEach((item) => {
        const row = document.createElement('tr');
        const cells = rowMapper(item);
        cells.forEach((value) => {
            const cell = document.createElement('td');
            cell.textContent = value ?? '';
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });
}

async function onAddBookClick() {
    const title = prompt('Tên sách mới:');
    if (!title) {
        return;
    }

    const author = prompt('Tác giả:');
    if (!author || !author.trim()) {
        alert('Vui lòng nhập tên tác giả.');
        return;
    }

    const category = prompt('Thể loại:');
    if (!category || !category.trim()) {
        alert('Vui lòng nhập thể loại.');
        return;
    }

    const pagesInput = prompt('Số trang:');
    const pages = Number.parseInt((pagesInput || '').trim(), 10);
    if (!Number.isInteger(pages) || pages <= 0) {
        alert('Số trang phải là số nguyên dương.');
        return;
    }

    const yearInput = prompt('Năm xuất bản:');
    const year = Number.parseInt((yearInput || '').trim(), 10);
    if (!Number.isInteger(year) || year <= 0) {
        alert('Năm xuất bản phải là số nguyên dương.');
        return;
    }

    const payload = {
        title: title.trim(),
        author: author.trim(),
        category: category.trim(),
        pages,
        year
    };

    try {
        await fetchJSON('/books', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        alert('Đã thêm sách mới thành công.');
        await Promise.all([loadBooks(), loadStats()]);
    } catch (error) {
        console.error('Không thể thêm sách:', error);
        alert(error?.message || 'Không thể thêm sách. Vui lòng thử lại sau.');
    }
}

async function onAddMemberClick() {
    const name = prompt('Tên thành viên mới:');
    if (!name || !name.trim()) {
        return;
    }
    try {
        await fetchJSON('/members', {
            method: 'POST',
            body: JSON.stringify({ name: name.trim() })
        });
        alert('Đã thêm thành viên mới.');
        await loadMembers();
        await loadStats();
    } catch (error) {
        console.error('Không thể thêm thành viên:', error);
        alert('Không thể thêm thành viên. Vui lòng thử lại sau.');
    }
}

function formatDate(value) {
    if (!value) return '—';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleDateString('vi-VN');
}

function debounce(fn, delay) {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), delay);
    };
}

async function onBorrowClick() {
    const memberIdRaw = prompt('Nhập ID thành viên:');
    const memberId = parseInt((memberIdRaw || '').trim(), 10);
    if (!memberId || Number.isNaN(memberId)) return;

    const keyword = prompt('Nhập từ khóa tên sách cần mượn:') || '';
    try {
        const list = await fetchJSON(`/books?q=${encodeURIComponent(keyword)}`);
        const available = Array.isArray(list) ? list.filter(b => b.status === 0 || b.statusText === 'Có sẵn') : [];
        if (available.length === 0) {
            alert('Không có sách có sẵn phù hợp.');
            return;
        }
        const lines = available.map(b => `[${b.bookId}] ${b.title} - ${b.author}`).join('\n');
        const pickRaw = prompt(`Chọn ID sách để mượn:\n${lines}`);
        const bookId = parseInt((pickRaw || '').trim(), 10);
        if (!bookId || Number.isNaN(bookId)) return;

        await fetchJSON('/borrowings/borrow', {
            method: 'POST',
            body: JSON.stringify({ memberId, bookId })
        });
        alert('Mượn sách thành công.');
        await Promise.all([loadBooks(), loadStats(), loadRecentBorrowings()]);
    } catch (e) {
        console.error(e);
        alert('Không thể mượn sách. Vui lòng thử lại sau.');
    }
}

async function onReturnClick() {
    const memberIdRaw = prompt('Nhập ID thành viên:');
    const memberId = parseInt((memberIdRaw || '').trim(), 10);
    if (!memberId || Number.isNaN(memberId)) return;

    try {
        const list = await fetchJSON(`/borrowings/current?memberId=${memberId}`);
        if (!Array.isArray(list) || list.length === 0) {
            alert('Thành viên này không có sách đang mượn.');
            return;
        }
        const lines = list.map(b => `[${b.bookId}] ${b.title} - ${b.author}`).join('\n');
        const pickRaw = prompt(`Chọn ID sách để trả:\n${lines}`);
        const bookId = parseInt((pickRaw || '').trim(), 10);
        if (!bookId || Number.isNaN(bookId)) return;

        await fetchJSON('/borrowings/return', {
            method: 'POST',
            body: JSON.stringify({ memberId, bookId })
        });
        alert('Trả sách thành công.');
        await Promise.all([loadBooks(), loadStats(), loadUpcomingDueDates()]);
    } catch (e) {
        console.error(e);
        alert('Không thể trả sách. Vui lòng thử lại sau.');
    }
}

