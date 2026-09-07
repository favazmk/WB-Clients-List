/**
 * Sales Team Client Directory - White Theme & Default Listing Style
 */

(function () {
  'use strict';

  // Category Icon Mapping for Instant Visual Recognition
  const CATEGORY_ICONS = {
    'All': 'fas fa-layer-group',
    'E-Commerce & Retail': 'fas fa-shopping-cart',
    'Food & Beverage / Dining': 'fas fa-utensils',
    'Fashion, Apparel & Textiles': 'fas fa-tshirt',
    'Corporate & Business Services': 'fas fa-briefcase',
    'Real Estate & Interior Design': 'fas fa-building',
    'Industrial, Trading & Engineering': 'fas fa-industry',
    'Health, Fitness & Wellness': 'fas fa-heartbeat',
    'Creative Agency & Media': 'fas fa-paint-brush',
    'Portfolios & Personal Brands': 'fas fa-user-tie',
    'Travel, Tourism & Hospitality': 'fas fa-plane-departure',
    'Luxury, Jewelry & Perfumes': 'fas fa-gem',
    'Technology & IT Solutions': 'fas fa-laptop-code',
    'Education & Community': 'fas fa-graduation-cap',
    'Gifts & Floral': 'fas fa-spa',
    'Entertainment & Media': 'fas fa-film'
  };

  // State Management: Default to 'table' (listing style) on every landing
  const state = {
    clients: CLIENTS_DATA || [],
    filteredClients: [],
    searchQuery: '',
    selectedCategory: 'All',
    selectedDomainType: 'all',
    selectedPlatform: 'all',
    selectedStatus: 'all',
    sortBy: 'name-asc',
    viewMode: 'table' // Always show listing style first when user lands
  };

  // Cached DOM Elements
  const elements = {
    // KPI Counters
    totalClientsCount: document.getElementById('totalClientsCount'),
    customDomainsCount: document.getElementById('customDomainsCount'),
    subdomainsCount: document.getElementById('subdomainsCount'),
    categoriesCount: document.getElementById('categoriesCount'),
    activeSitesCount: document.getElementById('activeSitesCount'),

    // Domain Tab Badges
    tabBadgeAll: document.getElementById('tabBadgeAll'),
    tabBadgeCustom: document.getElementById('tabBadgeCustom'),
    tabBadgeSub: document.getElementById('tabBadgeSub'),
    domainTabs: document.getElementById('domainTabs'),

    // Search & Filters
    searchInput: document.getElementById('searchInput'),
    clearSearchBtn: document.getElementById('clearSearchBtn'),
    filterPlatform: document.getElementById('filterPlatform'),
    filterStatus: document.getElementById('filterStatus'),
    sortBySelect: document.getElementById('sortBySelect'),
    categoryChipsContainer: document.getElementById('categoryChipsContainer'),

    // Results & Views
    resultsCount: document.getElementById('resultsCount'),
    resetAllBtn: document.getElementById('resetAllBtn'),
    gridContainer: document.getElementById('gridContainer'),
    tableContainer: document.getElementById('tableContainer'),
    tableBody: document.getElementById('tableBody'),
    emptyState: document.getElementById('emptyState'),
    resetEmptyBtn: document.getElementById('resetEmptyBtn'),

    // View Toggles
    gridViewBtn: document.getElementById('gridViewBtn'),
    tableViewBtn: document.getElementById('tableViewBtn'),

    // Actions & Feedback
    exportCsvBtn: document.getElementById('exportCsvBtn'),
    toastContainer: document.getElementById('toastContainer')
  };

  // Boot Application
  function init() {
    renderCategoryChips();
    updateKPIStats();
    applyFilters();
    setupEventListeners();
    applyViewMode(state.viewMode); // Always defaults to 'table' listing style
  }

  // Update Overview Numbers
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

    if (elements.tabBadgeAll) elements.tabBadgeAll.textContent = total;
    if (elements.tabBadgeCustom) elements.tabBadgeCustom.textContent = custom;
    if (elements.tabBadgeSub) elements.tabBadgeSub.textContent = sub;
  }

  // Render Visual Category Chips with Icons
  function renderCategoryChips() {
    if (!elements.categoryChipsContainer) return;

    const counts = { All: state.clients.length };
    state.clients.forEach(c => {
      counts[c.category] = (counts[c.category] || 0) + 1;
    });

    const sortedCategories = Object.keys(counts).filter(c => c !== 'All').sort();
    const categoriesList = ['All', ...sortedCategories];

    elements.categoryChipsContainer.innerHTML = categoriesList.map(cat => {
      const isActive = state.selectedCategory === cat ? 'active' : '';
      const iconClass = CATEGORY_ICONS[cat] || 'fas fa-tag';
      return `
        <button type="button" class="chip-btn ${isActive}" data-category="${escapeHtml(cat)}">
          <i class="${iconClass} chip-icon" aria-hidden="true"></i>
          <span>${escapeHtml(cat)}</span>
          <span class="chip-count">${counts[cat] || 0}</span>
        </button>
      `;
    }).join('');

    // Attach click listeners to chips
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

  // Filter & Sort Logic
  function applyFilters() {
    const q = state.searchQuery.trim().toLowerCase();

    state.filteredClients = state.clients.filter(client => {
      // Category filter
      if (state.selectedCategory !== 'All' && client.category !== state.selectedCategory) {
        return false;
      }

      // Domain type filter (All, Custom, Subdomain)
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

    sortClients();
    renderClients();
    updateResultsSummary();
  }

  // Sort Clients
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

  // Render Clients (Table Listing or Card Grid)
  function renderClients() {
    const count = state.filteredClients.length;

    if (count === 0) {
      if (elements.gridContainer) elements.gridContainer.style.display = 'none';
      if (elements.tableContainer) elements.tableContainer.style.display = 'none';
      if (elements.emptyState) elements.emptyState.style.display = 'block';
      return;
    }

    if (elements.emptyState) elements.emptyState.style.display = 'none';

    if (state.viewMode === 'table') {
      if (elements.gridContainer) elements.gridContainer.style.display = 'none';
      if (elements.tableContainer) elements.tableContainer.style.display = 'block';
      renderTableView();
    } else {
      if (elements.gridContainer) elements.gridContainer.style.display = 'grid';
      if (elements.tableContainer) elements.tableContainer.style.display = 'none';
      renderGridView();
    }
  }

  // Render Dense Table Listing View (Default)
  function renderTableView() {
    if (!elements.tableBody) return;

    elements.tableBody.innerHTML = state.filteredClients.map((client, index) => {
      const statusClass = getStatusClass(client.status);
      const isCustom = client.type === 'custom';
      const typeLabel = isCustom ? 'Custom' : 'Subdomain';
      const typeClass = isCustom ? 'custom' : 'subdomain';
      const platformIcon = client.platform === 'WordPress' ? 'fab fa-wordpress' : 'fas fa-code';
      const catIcon = CATEGORY_ICONS[client.category] || 'fas fa-tag';

      return `
        <tr id="row-${client.id}">
          <td style="color: var(--text-muted); font-size: 0.78rem; font-weight: 600;">${index + 1}</td>
          <td>
            <div class="table-client-title">${escapeHtml(client.name)}</div>
          </td>
          <td>
            <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="table-domain" title="Open website in new tab">
              <span>${escapeHtml(client.domain)}</span>
              <i class="fas fa-external-link-alt" style="font-size: 0.68rem; margin-left: 3px; opacity: 0.7;"></i>
            </a>
          </td>
          <td>
            <span class="card-category" style="font-size: 0.72rem; padding: 3px 8px;">
              <i class="${catIcon}" style="font-size: 0.7rem; color: var(--brand-primary);"></i>
              ${escapeHtml(client.category)}
            </span>
          </td>
          <td>
            <span class="card-type-tag ${typeClass}">${typeLabel}</span>
          </td>
          <td>
            <span style="display: inline-flex; align-items: center; gap: 5px; font-size: 0.8rem; color: var(--text-secondary); font-weight: 500;">
              <i class="${platformIcon}"></i> ${escapeHtml(client.platform)}
            </span>
          </td>
          <td>
            <span class="status-badge ${statusClass}">
              <span class="status-dot"></span> ${escapeHtml(client.status)}
            </span>
          </td>
          <td style="text-align: right;">
            <div class="table-actions" style="justify-content: flex-end;">
              <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary table-action-btn" title="Open Website">
                Visit ↗
              </a>
              <button type="button" class="btn table-action-btn" data-copy="${escapeHtml(client.domain)}" title="Copy Domain">
                <i class="far fa-copy"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

    attachCopyHandlers(elements.tableBody);
  }

  // Render Card Grid View (Alternative)
  function renderGridView() {
    if (!elements.gridContainer) return;

    elements.gridContainer.innerHTML = state.filteredClients.map(client => {
      const statusClass = getStatusClass(client.status);
      const isCustom = client.type === 'custom';
      const typeLabel = isCustom ? 'Custom Domain' : 'Staging Site';
      const typeClass = isCustom ? 'custom' : 'subdomain';
      const platformIcon = client.platform === 'WordPress' ? 'fab fa-wordpress' : 'fas fa-code';
      const catIcon = CATEGORY_ICONS[client.category] || 'fas fa-tag';

      return `
        <article class="client-card" id="${client.id}">
          <div class="card-header">
            <span class="card-category">
              <i class="${catIcon}" style="font-size: 0.72rem; color: var(--brand-primary);"></i>
              ${escapeHtml(client.category)}
            </span>
            <span class="status-badge ${statusClass}">
              <span class="status-dot"></span> ${escapeHtml(client.status)}
            </span>
          </div>

          <h3 class="card-title">${escapeHtml(client.name)}</h3>

          <!-- Domain Box -->
          <div class="card-domain-box">
            <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="card-domain-link" title="Open ${escapeHtml(client.domain)}">
              <i class="fas fa-globe" style="font-size: 0.76rem; opacity: 0.7;"></i>
              <span>${escapeHtml(client.domain)}</span>
            </a>
            <button type="button" class="copy-icon-btn" data-copy="${escapeHtml(client.domain)}" title="Copy domain">
              <i class="far fa-copy"></i>
            </button>
          </div>

          <div class="card-meta">
            <span class="platform-pill">
              <i class="${platformIcon}"></i> ${escapeHtml(client.platform)}
            </span>
            <span class="card-type-tag ${typeClass}">
              ${typeLabel}
            </span>
          </div>

          <!-- Primary Visit Button -->
          <a href="${escapeHtml(client.url)}" target="_blank" rel="noopener noreferrer" class="open-site-btn">
            <span>Open Website</span>
            <i class="fas fa-arrow-up-right-from-square" style="font-size: 0.75rem;"></i>
          </a>
        </article>
      `;
    }).join('');

    attachCopyHandlers(elements.gridContainer);
  }

  // Copy Handlers with Visual Toast Feedback
  function attachCopyHandlers(container) {
    container.querySelectorAll('[data-copy]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const text = btn.getAttribute('data-copy');
        copyToClipboard(text);
      });
    });
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied "${text}" to clipboard!`);
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
      showToast(`Copied "${text}" to clipboard!`);
    } catch (err) {
      showToast(`Failed to copy: ${text}`, 'error');
    }
    document.body.removeChild(input);
  }

  // Toast Notification System
  function showToast(message, type = 'success') {
    if (!elements.toastContainer) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    const icon = type === 'success' ? 'fas fa-check-circle toast-icon' : 'fas fa-exclamation-circle toast-icon';
    toast.innerHTML = `<i class="${icon}"></i><span>${escapeHtml(message)}</span>`;

    elements.toastContainer.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 250);
    }, 2400);
  }

  // Update Result Count Text & Reset Link
  function updateResultsSummary() {
    const total = state.clients.length;
    const count = state.filteredClients.length;

    if (elements.resultsCount) {
      elements.resultsCount.innerHTML = `Showing <span class="results-count-highlight">${count}</span> of ${total} clients`;
    }

    const hasActiveFilters = state.searchQuery ||
      state.selectedCategory !== 'All' ||
      state.selectedDomainType !== 'all' ||
      state.selectedPlatform !== 'all' ||
      state.selectedStatus !== 'all';

    if (elements.resetAllBtn) {
      elements.resetAllBtn.style.display = hasActiveFilters ? 'inline-block' : 'none';
    }
  }

  // View Switching
  function applyViewMode(mode) {
    state.viewMode = mode;

    if (elements.tableViewBtn) elements.tableViewBtn.classList.toggle('active', mode === 'table');
    if (elements.gridViewBtn) elements.gridViewBtn.classList.toggle('active', mode === 'grid');

    renderClients();
  }

  // Export to CSV
  function exportToCSV() {
    const list = state.filteredClients.length > 0 ? state.filteredClients : state.clients;
    const headers = ['ID', 'Client Name', 'Website Domain', 'Direct URL', 'Category', 'Domain Type', 'Platform', 'Status'];
    const rows = list.map(c => [
      c.id,
      `"${c.name.replace(/"/g, '""')}"`,
      `"${c.domain}"`,
      `"${c.url}"`,
      `"${c.category.replace(/"/g, '""')}"`,
      `"${c.type}"`,
      `"${c.platform}"`,
      `"${c.status}"`
    ]);

    const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Agency_Clients_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast(`Exported ${list.length} clients to CSV`);
  }

  // Setup Event Listeners
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

    // Keyboard Shortcuts: "/" focuses search, "Esc" blurs
    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== elements.searchInput) {
        e.preventDefault();
        if (elements.searchInput) elements.searchInput.focus();
      }
      if (e.key === 'Escape' && document.activeElement === elements.searchInput) {
        elements.searchInput.blur();
      }
    });

    // Domain Segmented Tabs (All / Custom / Subdomain)
    if (elements.domainTabs) {
      elements.domainTabs.querySelectorAll('.domain-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const type = btn.getAttribute('data-type');
          state.selectedDomainType = type;
          elements.domainTabs.querySelectorAll('.domain-tab-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          applyFilters();
        });
      });
    }

    // Platform Filter
    if (elements.filterPlatform) {
      elements.filterPlatform.addEventListener('change', (e) => {
        state.selectedPlatform = e.target.value;
        applyFilters();
      });
    }

    // Status Filter
    if (elements.filterStatus) {
      elements.filterStatus.addEventListener('change', (e) => {
        state.selectedStatus = e.target.value;
        applyFilters();
      });
    }

    // Sort Dropdown
    if (elements.sortBySelect) {
      elements.sortBySelect.addEventListener('change', (e) => {
        state.sortBy = e.target.value;
        applyFilters();
      });
    }

    // View Toggles: Table (Listing) vs Grid (Cards)
    if (elements.tableViewBtn) {
      elements.tableViewBtn.addEventListener('click', () => applyViewMode('table'));
    }
    if (elements.gridViewBtn) {
      elements.gridViewBtn.addEventListener('click', () => applyViewMode('grid'));
    }

    // Reset Buttons
    if (elements.resetAllBtn) {
      elements.resetAllBtn.addEventListener('click', resetAllFilters);
    }
    if (elements.resetEmptyBtn) {
      elements.resetEmptyBtn.addEventListener('click', resetAllFilters);
    }

    // Export CSV
    if (elements.exportCsvBtn) {
      elements.exportCsvBtn.addEventListener('click', exportToCSV);
    }
  }

  // Reset Filters to Default
  function resetAllFilters() {
    state.searchQuery = '';
    state.selectedCategory = 'All';
    state.selectedDomainType = 'all';
    state.selectedPlatform = 'all';
    state.selectedStatus = 'all';
    state.sortBy = 'name-asc';

    if (elements.searchInput) elements.searchInput.value = '';
    if (elements.clearSearchBtn) elements.clearSearchBtn.style.display = 'none';
    if (elements.filterPlatform) elements.filterPlatform.value = 'all';
    if (elements.filterStatus) elements.filterStatus.value = 'all';
    if (elements.sortBySelect) elements.sortBySelect.value = 'name-asc';

    if (elements.domainTabs) {
      elements.domainTabs.querySelectorAll('.domain-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-type') === 'all');
      });
    }

    if (elements.categoryChipsContainer) {
      elements.categoryChipsContainer.querySelectorAll('.chip-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-category') === 'All');
      });
    }

    applyFilters();
    showToast('Filters reset to show all clients');
  }

  // Helper Functions
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

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Initialize on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
