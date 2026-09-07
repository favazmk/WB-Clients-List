/**
 * Sales Team Client Directory - Application Logic
 * Fast client-side searching, multi-criteria filtering, sorting, view switching, and CSV export.
 */

(function () {
  'use strict';

  // Application State
  const state = {
    clients: CLIENTS_DATA || [],
    filteredClients: [],
    searchQuery: '',
    selectedCategory: 'All',
    selectedDomainType: 'all',
    selectedPlatform: 'all',
    selectedStatus: 'all',
    sortBy: 'name-asc',
    viewMode: localStorage.getItem('wb_view_mode') || 'grid',
    theme: localStorage.getItem('wb_theme') || 'dark'
  };

  // DOM Elements Cache
  const elements = {
    // Stats
    totalClientsCount: document.getElementById('totalClientsCount'),
    customDomainsCount: document.getElementById('customDomainsCount'),
    subdomainsCount: document.getElementById('subdomainsCount'),
    categoriesCount: document.getElementById('categoriesCount'),
    activeSitesCount: document.getElementById('activeSitesCount'),

    // Search & Filters
    searchInput: document.getElementById('searchInput'),
    clearSearchBtn: document.getElementById('clearSearchBtn'),
    filterDomainType: document.getElementById('filterDomainType'),
    filterPlatform: document.getElementById('filterPlatform'),
    filterStatus: document.getElementById('filterStatus'),
    sortBySelect: document.getElementById('sortBySelect'),
    categoryChipsContainer: document.getElementById('categoryChipsContainer'),

    // View Controls
    resultsCount: document.getElementById('resultsCount'),
    activeFilterTag: document.getElementById('activeFilterTag'),
    resetAllBtn: document.getElementById('resetAllBtn'),
    gridContainer: document.getElementById('gridContainer'),
    tableContainer: document.getElementById('tableContainer'),
    tableBody: document.getElementById('tableBody'),
    emptyState: document.getElementById('emptyState'),
    resetEmptyBtn: document.getElementById('resetEmptyBtn'),

    // View Toggles
    gridViewBtn: document.getElementById('gridViewBtn'),
    tableViewBtn: document.getElementById('tableViewBtn'),

    // Actions
    exportCsvBtn: document.getElementById('exportCsvBtn'),
    themeToggleBtn: document.getElementById('themeToggleBtn'),
    toastContainer: document.getElementById('toastContainer')
  };

  // Initialize
  function init() {
    applyTheme(state.theme);
    renderCategoryChips();
    updateKPIStats();
    applyFilters();
    setupEventListeners();
    applyViewMode(state.viewMode);
  }

  // Calculate & Update KPI Stats
  function updateKPIStats() {
    const total = state.clients.length;
    const custom = state.clients.filter(c => c.type === 'custom').length;
    const sub = state.clients.filter(c => c.type === 'subdomain').length;
    const categories = new Set(state.clients.map(c => c.category)).size;
    const active = state.clients.filter(c => c.status === 'Active').length;

    if (elements.totalClientsCount) elements.totalClientsCount.textContent = total;
    if (elements.customDomainsCount) elements.customDomainsCount.textContent = custom;
    if (elements.subdomainsCount) elements.subdomainsCount.textContent = sub;
    if (elements.categoriesCount) elements.categoriesCount.textContent = categories;
    if (elements.activeSitesCount) elements.activeSitesCount.textContent = active;
  }

  // Render Category Filter Chips with counts
  function renderCategoryChips() {
    if (!elements.categoryChipsContainer) return;

    // Count categories
    const counts = { All: state.clients.length };
    state.clients.forEach(c => {
      counts[c.category] = (counts[c.category] || 0) + 1;
    });

    // Unique sorted categories
    const categories = Object.keys(counts).filter(c => c !== 'All').sort();
    const allCategories = ['All', ...categories];

    elements.categoryChipsContainer.innerHTML = allCategories.map(cat => {
      const isActive = state.selectedCategory === cat ? 'active' : '';
      return `
        <button type="button" class="chip-btn ${isActive}" data-category="${escapeHtml(cat)}">
          <span>${escapeHtml(cat)}</span>
          <span class="chip-count">${counts[cat] || 0}</span>
        </button>
      `;
    }).join('');

    // Attach click events
    elements.categoryChipsContainer.querySelectorAll('.chip-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cat = btn.getAttribute('data-category');
        state.selectedCategory = cat;
        elements.categoryChipsContainer.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyFilters();
      });
    });
  }

  // Filter and Sort Logic
  function applyFilters() {
    const q = state.searchQuery.trim().toLowerCase();

    state.filteredClients = state.clients.filter(client => {
      // Category filter
      if (state.selectedCategory !== 'All' && client.category !== state.selectedCategory) {
        return false;
      }

      // Domain type filter
      if (state.selectedDomainType !== 'all' && client.type !== state.selectedDomainType) {
        return false;
      }

      // Platform filter
      if (state.selectedPlatform !== 'all' && client.platform !== state.selectedPlatform) {
        return false;
      }

      // Status filter
      if (state.selectedStatus !== 'all' && client.status !== state.selectedStatus) {
        return false;
      }

      // Search Query
      if (q) {
        const matchName = client.name.toLowerCase().includes(q);
        const matchDomain = client.domain.toLowerCase().includes(q);
        const matchCategory = client.category.toLowerCase().includes(q);
        const matchPlatform = client.platform.toLowerCase().includes(q);
        const matchTags = client.tags && client.tags.some(t => t.toLowerCase().includes(q));
        if (!matchName && !matchDomain && !matchCategory && !matchPlatform && !matchTags) {
          return false;
        }
      }

      return true;
    });

    // Sort
    sortClients();

    // Render results
    renderClients();
    updateResultsSummary();
  }

  // Sort Array
  function sortClients() {
    state.filteredClients.sort((a, b) => {
      switch (state.sortBy) {
        case 'name-asc':
          return a.name.localeCompare(b.name);
        case 'name-desc':
          return b.name.localeCompare(a.name);
        case 'category-asc':
          return a.category.localeCompare(b.category) || a.name.localeCompare(b.name);
        case 'domain-asc':
          return a.domain.localeCompare(b.domain);
        case 'status-asc':
          return a.status.localeCompare(b.status) || a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });
  }

  // Render Grid and Table
  function renderClients() {
    const count = state.filteredClients.length;

    if (count === 0) {
      if (elements.gridContainer) elements.gridContainer.style.display = 'none';
      if (elements.tableContainer) elements.tableContainer.style.display = 'none';
      if (elements.emptyState) elements.emptyState.style.display = 'block';
      return;
    }

    if (elements.emptyState) elements.emptyState.style.display = 'none';

    if (state.viewMode === 'grid') {
      if (elements.gridContainer) elements.gridContainer.style.display = 'grid';
      if (elements.tableContainer) elements.tableContainer.style.display = 'none';
      renderGridView();
    } else {
      if (elements.gridContainer) elements.gridContainer.style.display = 'none';
      if (elements.tableContainer) elements.tableContainer.style.display = 'block';
      renderTableView();
    }
  }

  // Render Grid Cards
  function renderGridView() {
    if (!elements.gridContainer) return;

    elements.gridContainer.innerHTML = state.filteredClients.map(client => {
      const statusClass = getStatusClass(client.status);
      const isCustom = client.type === 'custom';
      const typeLabel = isCustom ? 'Custom Domain' : 'Staging / Subdomain';
      const typeClass = isCustom ? 'custom' : 'subdomain';
      const platformIcon = client.platform === 'WordPress' ? 'fab fa-wordpress' : 'fas fa-code';

      return `
        <article class="client-card" id="${client.id}">
          <div class="card-top">
            <span class="card-category-badge">${escapeHtml(client.category)}</span>
            <div class="card-badges-row">
              <span class="type-pill ${typeClass}">${typeLabel}</span>
            </div>
          </div>

          <h3 class="card-title">${escapeHtml(client.name)}</h3>

          <div class="card-domain-box">
            <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="card-domain-link" title="Open ${escapeHtml(client.domain)} in new tab">
              <i class="fas fa-globe" style="margin-right: 6px; font-size: 0.8rem; opacity: 0.7;"></i>${escapeHtml(client.domain)}
            </a>
            <button type="button" class="copy-domain-btn" data-copy="${escapeHtml(client.domain)}" title="Copy domain to clipboard">
              <i class="far fa-copy"></i>
            </button>
          </div>

          <div class="card-meta-list">
            <div class="card-meta-item">
              <span class="meta-key">Platform</span>
              <span class="meta-val">
                <i class="${platformIcon}"></i> ${escapeHtml(client.platform)}
              </span>
            </div>
            <div class="card-meta-item">
              <span class="meta-key">Status</span>
              <span class="status-pill ${statusClass}">
                <span class="status-dot"></span> ${escapeHtml(client.status)}
              </span>
            </div>
          </div>

          <div class="card-actions">
            <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="visit-btn">
              <span>Visit Site</span>
              <i class="fas fa-external-link-alt" style="font-size: 0.75rem;"></i>
            </a>
            <button type="button" class="copy-action-btn" data-copy="${escapeHtml(client.url)}" title="Copy Full Website URL">
              <i class="fas fa-link"></i>
            </button>
          </div>
        </article>
      `;
    }).join('');

    attachCopyHandlers(elements.gridContainer);
  }

  // Render Dense Table
  function renderTableView() {
    if (!elements.tableBody) return;

    elements.tableBody.innerHTML = state.filteredClients.map((client, index) => {
      const statusClass = getStatusClass(client.status);
      const isCustom = client.type === 'custom';
      const typeLabel = isCustom ? 'Custom' : 'Subdomain';
      const typeClass = isCustom ? 'custom' : 'subdomain';
      const platformIcon = client.platform === 'WordPress' ? 'fab fa-wordpress' : 'fas fa-code';

      return `
        <tr id="row-${client.id}">
          <td style="color: var(--text-muted); font-size: 0.8rem;">#${index + 1}</td>
          <td>
            <div class="table-client-name">${escapeHtml(client.name)}</div>
          </td>
          <td>
            <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="table-domain-link" title="Open in new tab">
              ${escapeHtml(client.domain)}
              <i class="fas fa-external-link-alt" style="font-size: 0.7rem; margin-left: 2px;"></i>
            </a>
          </td>
          <td>
            <span class="card-category-badge" style="font-size: 0.72rem; padding: 2px 8px;">${escapeHtml(client.category)}</span>
          </td>
          <td>
            <span class="type-pill ${typeClass}">${typeLabel}</span>
          </td>
          <td>
            <span style="display: inline-flex; align-items: center; gap: 5px; font-size: 0.82rem;">
              <i class="${platformIcon}"></i> ${escapeHtml(client.platform)}
            </span>
          </td>
          <td>
            <span class="status-pill ${statusClass}">
              <span class="status-dot"></span> ${escapeHtml(client.status)}
            </span>
          </td>
          <td>
            <div class="table-actions">
              <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary table-btn" title="Visit Website">
                Visit ↗
              </a>
              <button type="button" class="btn table-btn" data-copy="${escapeHtml(client.domain)}" title="Copy Domain">
                <i class="far fa-copy"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

    attachCopyHandlers(elements.tableBody);
  }

  // Attach Copy Buttons
  function attachCopyHandlers(container) {
    container.querySelectorAll('[data-copy]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const textToCopy = btn.getAttribute('data-copy');
        copyToClipboard(textToCopy);
      });
    });
  }

  // Copy to Clipboard
  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied to clipboard: "${text}"`);
      }).catch(() => {
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    const input = document.createElement('input');
    input.value = text;
    document.body.appendChild(input);
    input.select();
    try {
      document.execCommand('copy');
      showToast(`Copied to clipboard: "${text}"`);
    } catch (err) {
      showToast(`Failed to copy: "${text}"`, 'error');
    }
    document.body.removeChild(input);
  }

  // Toast System
  function showToast(message, type = 'success') {
    if (!elements.toastContainer) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    const iconClass = type === 'success' ? 'fas fa-check-circle toast-icon' : 'fas fa-exclamation-circle toast-icon';
    toast.innerHTML = `<i class="${iconClass}"></i><span>${escapeHtml(message)}</span>`;

    elements.toastContainer.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 2800);
  }

  // Update Results Bar Summary
  function updateResultsSummary() {
    const total = state.clients.length;
    const current = state.filteredClients.length;

    if (elements.resultsCount) {
      elements.resultsCount.innerHTML = `Showing <span class="results-count-number">${current}</span> of ${total} clients`;
    }

    const hasFilters = state.searchQuery ||
      state.selectedCategory !== 'All' ||
      state.selectedDomainType !== 'all' ||
      state.selectedPlatform !== 'all' ||
      state.selectedStatus !== 'all';

    if (elements.resetAllBtn) {
      elements.resetAllBtn.style.display = hasFilters ? 'inline-block' : 'none';
    }
  }

  // Switch View Mode (Grid vs Table)
  function applyViewMode(mode) {
    state.viewMode = mode;
    localStorage.setItem('wb_view_mode', mode);

    if (elements.gridViewBtn) elements.gridViewBtn.classList.toggle('active', mode === 'grid');
    if (elements.tableViewBtn) elements.tableViewBtn.classList.toggle('active', mode === 'table');

    renderClients();
  }

  // Export Filtered Clients to CSV
  function exportToCSV() {
    const dataToExport = state.filteredClients.length > 0 ? state.filteredClients : state.clients;

    const headers = ['ID', 'Client Name', 'Domain', 'Website URL', 'Category', 'Domain Type', 'Platform', 'Status', 'Tags'];
    const rows = dataToExport.map(c => [
      c.id,
      `"${c.name.replace(/"/g, '""')}"`,
      `"${c.domain}"`,
      `"${c.url}"`,
      `"${c.category.replace(/"/g, '""')}"`,
      `"${c.type}"`,
      `"${c.platform}"`,
      `"${c.status}"`,
      `"${(c.tags || []).join(', ')}"`
    ]);

    const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `Agency_Clients_Directory_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast(`Exported ${dataToExport.length} clients to CSV`);
  }

  // Theme Switching
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('wb_theme', theme);

    if (elements.themeToggleBtn) {
      const icon = elements.themeToggleBtn.querySelector('i');
      if (icon) {
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
      }
    }
  }

  function toggleTheme() {
    const nextTheme = state.theme === 'light' ? 'dark' : 'light';
    applyTheme(nextTheme);
  }

  // Event Listeners
  function setupEventListeners() {
    // Search input
    if (elements.searchInput) {
      elements.searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value;
        if (elements.clearSearchBtn) {
          elements.clearSearchBtn.style.display = state.searchQuery ? 'block' : 'none';
        }
        applyFilters();
      });

      // Clear search
      if (elements.clearSearchBtn) {
        elements.clearSearchBtn.addEventListener('click', () => {
          elements.searchInput.value = '';
          state.searchQuery = '';
          elements.clearSearchBtn.style.display = 'none';
          elements.searchInput.focus();
          applyFilters();
        });
      }
    }

    // Keyboard shortcut: Press "/" to focus search
    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== elements.searchInput) {
        e.preventDefault();
        if (elements.searchInput) {
          elements.searchInput.focus();
        }
      }
      if (e.key === 'Escape' && document.activeElement === elements.searchInput) {
        elements.searchInput.blur();
      }
    });

    // Secondary Filter selects
    if (elements.filterDomainType) {
      elements.filterDomainType.addEventListener('change', (e) => {
        state.selectedDomainType = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterPlatform) {
      elements.filterPlatform.addEventListener('change', (e) => {
        state.selectedPlatform = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterStatus) {
      elements.filterStatus.addEventListener('change', (e) => {
        state.selectedStatus = e.target.value;
        applyFilters();
      });
    }

    // Sort select
    if (elements.sortBySelect) {
      elements.sortBySelect.addEventListener('change', (e) => {
        state.sortBy = e.target.value;
        applyFilters();
      });
    }

    // View mode buttons
    if (elements.gridViewBtn) {
      elements.gridViewBtn.addEventListener('click', () => applyViewMode('grid'));
    }
    if (elements.tableViewBtn) {
      elements.tableViewBtn.addEventListener('click', () => applyViewMode('table'));
    }

    // Reset buttons
    if (elements.resetAllBtn) {
      elements.resetAllBtn.addEventListener('click', resetAllFilters);
    }
    if (elements.resetEmptyBtn) {
      elements.resetEmptyBtn.addEventListener('click', resetAllFilters);
    }

    // Export to CSV
    if (elements.exportCsvBtn) {
      elements.exportCsvBtn.addEventListener('click', exportToCSV);
    }

    // Theme toggle
    if (elements.themeToggleBtn) {
      elements.themeToggleBtn.addEventListener('click', toggleTheme);
    }
  }

  // Reset all filters to default
  function resetAllFilters() {
    state.searchQuery = '';
    state.selectedCategory = 'All';
    state.selectedDomainType = 'all';
    state.selectedPlatform = 'all';
    state.selectedStatus = 'all';
    state.sortBy = 'name-asc';

    if (elements.searchInput) elements.searchInput.value = '';
    if (elements.clearSearchBtn) elements.clearSearchBtn.style.display = 'none';
    if (elements.filterDomainType) elements.filterDomainType.value = 'all';
    if (elements.filterPlatform) elements.filterPlatform.value = 'all';
    if (elements.filterStatus) elements.filterStatus.value = 'all';
    if (elements.sortBySelect) elements.sortBySelect.value = 'name-asc';

    if (elements.categoryChipsContainer) {
      elements.categoryChipsContainer.querySelectorAll('.chip-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-category') === 'All');
      });
    }

    applyFilters();
    showToast('Filters reset');
  }

  // Helpers
  function getStatusClass(status) {
    switch (status) {
      case 'Active':
        return 'status-active';
      case 'Pending Setup':
        return 'status-pending';
      case 'Domain Pending Purchase':
        return 'status-purchase';
      case 'Expiring Soon':
      case 'Needs Attention':
      case 'Issue / Offline':
        return 'status-issue';
      default:
        return 'status-active';
    }
  }

  function escapeHtml(string) {
    if (!string) return '';
    return String(string)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Boot on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
