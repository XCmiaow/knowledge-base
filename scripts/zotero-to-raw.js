/**
 * Zotero → knowledge-base/raw/ 导出脚本
 *
 * 用法:
 *   1. 在 Zotero 中选中文献
 *   2. 运行此脚本 (需要 Zotero 的 Better BibTeX + 自定义导出)
 *   3. JSON 文件自动写入 knowledge-base/raw/<主题>/
 *
 * 或者通过 Zotero Local API 调用:
 *   curl http://localhost:23119/api/items/top?limit=50 > raw/export.json
 */

// Zotero Local API 端点
const ZOTERO_API = 'http://localhost:23119/api';
const RAW_DIR = 'E:/工作区/knowledge-base/raw';

// 主题关键词 → 目录映射
const TOPIC_MAP = {
  hydrogel: '水凝胶',
  'anti-freeze': '水凝胶',
  cellulose: '水凝胶',
  '柔性电子': '水凝胶',
  水凝胶: '水凝胶',
  'organophosphorus': '有机磷化学',
  'organophosphor': '有机磷化学',
  '手性膦': '有机磷化学',
  'cheminformatics': '化学信息学',
  'chemoinformatics': '化学信息学',
  'machine learning': '化学信息学',
  '化工设计': '化工设计竞赛',
  '苯乙烯': '化工设计竞赛',
};

function guessTopic(item) {
  const text = [
    item.title,
    item.tags?.map(t => t.tag || t).join(' '),
    item.extra,
    item.abstractNote
  ].filter(Boolean).join(' ').toLowerCase();

  for (const [keyword, topic] of Object.entries(TOPIC_MAP)) {
    if (text.includes(keyword.toLowerCase())) return topic;
  }
  return '其他';
}

async function exportItems() {
  const resp = await fetch(`${ZOTERO_API}/items/top?limit=100&sort=dateAdded&direction=desc`);
  const items = await resp.json();

  for (const item of items) {
    const data = item.data;
    const topic = guessTopic(data);
    const doi = data.DOI?.replace(/[\/\\:]/g, '_') || data.key;

    const record = {
      doi: data.DOI || '',
      title_en: data.title || '',
      title_zh: '',
      url: data.url || data.DOI ? `https://doi.org/${data.DOI}` : '',
      date: data.dateAdded?.split(' ')[0] || new Date().toISOString().split('T')[0],
      authors: data.creators?.map(c => `${c.lastName}, ${c.firstName}`) || [],
      journal: data.publicationTitle || '',
      year: data.date?.match(/\d{4}/)?.[0] || '',
      abstract: data.abstractNote || '',
      tags: data.tags?.map(t => t.tag || t) || [],
      extra: data.extra || '',
      zotero_key: data.key,
    };

    const filename = `${doi || data.key}.json`;
    const dir = `${RAW_DIR}/${topic}`;

    // Ensure directory exists
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(`${dir}/${filename}`, JSON.stringify(record, null, 2));
    console.log(`✓ ${topic}/${filename}`);
  }
}

exportItems().catch(console.error);
