import PDFDocument from 'pdfkit';
import { createWriteStream } from 'fs';

// Page layout constants (Letter size: 612 x 792 points)
const PAGE = {
  width: 612,
  height: 792,
  margin: 20,
  gutter: 10
};

// Card dimensions (5x2 grid = 10 per page)
const CARD = {
  width: (PAGE.width - PAGE.margin * 2 - PAGE.gutter) / 2,
  height: (PAGE.height - PAGE.margin * 2 - PAGE.gutter * 4) / 5
};

// Colors
const COLORS = {
  headerBg: '#1a365d',      // Dark blue
  headerText: '#ffffff',
  statsBg: '#d0d8e4',       // Slightly darker gray for better contrast
  statsLabelBg: '#b8c4d4',  // Darker for stat labels
  sectionHeader: '#2d3748', // Dark gray
  text: '#1a202c',
  lightText: '#4a5568',
  border: '#cbd5e0',
  accent: '#3182ce',        // Blue accent
  cpBg: '#2b6cb0',          // CP badge bg
  cpText: '#ffffff',
  // Stratagem alternating backgrounds
  stratagemOdd: '#ffffff',
  stratagemEven: '#f7fafc'  // Very light blue-gray
};

// Fonts
const FONT = {
  regular: 'Helvetica',
  bold: 'Helvetica-Bold'
};

export async function generatePDF(data, outputPath, options = {}) {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({
      size: 'letter',
      margins: { top: PAGE.margin, bottom: PAGE.margin, left: PAGE.margin, right: PAGE.margin }
    });

    const stream = createWriteStream(outputPath);
    doc.pipe(stream);

    // Page 1+: Datasheet cards (10 per page, unique units only) - NO title page
    if (options.includeDatasheets !== false) {
      const units = data.units;
      for (let i = 0; i < units.length; i += 10) {
        if (i > 0) doc.addPage();
        const pageUnits = units.slice(i, i + 10);
        pageUnits.forEach((unit, idx) => {
          const col = idx % 2;
          const row = Math.floor(idx / 2);
          const x = PAGE.margin + col * (CARD.width + PAGE.gutter);
          const y = PAGE.margin + row * (CARD.height + PAGE.gutter);
          renderUnitCard(doc, unit, x, y);
        });
      }
    }

    // Stratagems page (stacked vertically, bigger text)
    if ((options.includeCoreStrats && data.coreStratagems) || (options.includeDetachmentStrats && data.detachmentStratagems)) {
      doc.addPage();
      renderStratagemsPage(doc, data, options);
    }

    // Reference page: Keywords, Points, then Faction/Detachment rules
    if ((options.includeKeywords && data.keywords) || (options.includePoints && data.pointsSummary)) {
      doc.addPage();
      renderReferencePage(doc, data, options);
    }

    doc.end();

    stream.on('finish', resolve);
    stream.on('error', reject);
  });
}

// No longer expanding units - each unit type appears once with qty indicator

// No title page - jump straight to content

function renderUnitCard(doc, unit, x, y) {
  const padding = 2;
  const innerWidth = CARD.width - padding * 2;
  const qty = unit.qty || 1;

  // Card border
  doc.rect(x, y, CARD.width, CARD.height).stroke(COLORS.border);

  // Header bar with unit name and points
  doc.rect(x, y, CARD.width, 14).fill(COLORS.headerBg);
  doc.font(FONT.bold).fontSize(10).fillColor(COLORS.headerText);
  const nameText = qty > 1 ? `${unit.name.toUpperCase()} x${qty}` : unit.name.toUpperCase();
  doc.text(nameText, x + padding + 1, y + 2, { width: innerWidth - 35, lineBreak: false });
  doc.text(`${unit.pts}`, x + CARD.width - 32, y + 2, { width: 30, align: 'right', lineBreak: false });

  let currentY = y + 15;

  // Stats bar - large and prominent
  const stats = unit.stats;
  const statWidth = innerWidth / 8;
  const statsHeight = 22;

  doc.rect(x + padding, currentY, innerWidth, statsHeight).fill(COLORS.statsBg);

  const statLabels = ['M', 'T', 'SV', 'W', 'LD', 'OC', 'INV', 'FNP'];
  const statValues = [
    stats.M || '-', stats.T || '-', stats.SV || '-', stats.W || '-',
    stats.LD || '-', stats.OC ?? '-', stats.INV || '-', stats.FNP || '-'
  ];

  statLabels.forEach((label, i) => {
    const sx = x + padding + i * statWidth;
    doc.font(FONT.bold).fontSize(7).fillColor(COLORS.lightText);
    doc.text(label, sx, currentY + 1, { width: statWidth, align: 'center', lineBreak: false });
    doc.font(FONT.bold).fontSize(12).fillColor(COLORS.text);
    doc.text(String(statValues[i]), sx, currentY + 9, { width: statWidth, align: 'center', lineBreak: false });
  });

  currentY += statsHeight + 1;

  // Calculate space for content
  const footerHeight = 12;
  const contentEnd = y + CARD.height - footerHeight;
  const contentSpace = contentEnd - currentY;

  // Show ALL weapons - scale font to fit
  const weaponCount = unit.weapons.length;
  const abilityCount = unit.abilities.length;
  const totalLines = weaponCount + abilityCount;

  // Determine font size based on how much we need to fit
  let fontSize = 9;
  let lineHeight = 11;
  if (totalLines > 7) {
    fontSize = 7;
    lineHeight = 9;
  } else if (totalLines > 5) {
    fontSize = 8;
    lineHeight = 10;
  }

  // ALL Weapons - full names, no clipping
  for (const wpn of unit.weapons) {
    if (currentY + lineHeight > contentEnd) break;
    doc.font(FONT.bold).fontSize(fontSize).fillColor(COLORS.text);
    doc.text(`${wpn.name}: `, x + padding, currentY, { continued: true, lineBreak: false });
    doc.font(FONT.regular).fontSize(fontSize).fillColor(COLORS.text);
    const profileText = wpn.tags.length > 0 ? `${wpn.profile} [${wpn.tags.join(',')}]` : wpn.profile;
    doc.text(profileText, { lineBreak: false });
    currentY += lineHeight;
  }

  // Abilities
  for (const ability of unit.abilities) {
    if (currentY + lineHeight > contentEnd) break;
    doc.font(FONT.regular).fontSize(fontSize).fillColor(COLORS.text);
    doc.text(`• ${ability}`, x + padding, currentY, { width: innerWidth, lineBreak: false, ellipsis: true });
    currentY += lineHeight;
  }

  // Footer: Core keywords + Leads + important keywords
  const bottomY = y + CARD.height - footerHeight;
  const footerParts = [];

  // Core abilities (Deep Strike, Leader, Deadly Demise, Infiltrators, Scouts, etc.)
  if (unit.core && unit.core.length > 0) {
    footerParts.push(unit.core.join(', '));
  }

  // Add Leads info
  if (unit.leads && unit.leads.length > 0) {
    footerParts.push(`→${unit.leads.join(', ')}`);
  }

  // Add notes
  if (unit.notes) footerParts.push(unit.notes);

  if (footerParts.length > 0) {
    doc.font(FONT.bold).fontSize(7).fillColor(COLORS.accent);
    doc.text(footerParts.join(' | '), x + padding, bottomY, { width: innerWidth, lineBreak: false, ellipsis: true });
  }
}

function renderStratagemCard(doc, strat, x, y, width, height, index = 0) {
  const padding = 5;
  const innerWidth = width - padding * 2;

  // Card background (alternating)
  const bgColor = index % 2 === 0 ? COLORS.stratagemOdd : COLORS.stratagemEven;
  doc.rect(x, y, width, height).fill(bgColor).stroke(COLORS.border);

  // CP badge on left
  doc.font(FONT.bold).fontSize(10).fillColor(COLORS.cpBg);
  doc.text(`${strat.cp}CP`, x + padding, y + 4, { width: 28 });

  // Stratagem name
  doc.font(FONT.bold).fontSize(10).fillColor(COLORS.headerBg);
  doc.text(strat.name.toUpperCase(), x + 38, y + 4, { width: innerWidth - 38 });

  // Phase on same line, right-aligned
  const phaseText = strat.type ? `${strat.phase} | ${strat.type}` : strat.phase;
  doc.font(FONT.regular).fontSize(7).fillColor(COLORS.accent);
  doc.text(phaseText, x + width - 100, y + 6, { width: 95, align: 'right' });

  // Effect - bigger font
  doc.font(FONT.regular).fontSize(9).fillColor(COLORS.text);
  doc.text(strat.effect, x + padding, y + 18, { width: innerWidth, height: height - 22 });
}

function renderStratagemsPage(doc, data, options) {
  const contentWidth = PAGE.width - PAGE.margin * 2;
  let y = PAGE.margin;

  // Combine all stratagems vertically
  const allStrats = [];

  if (options.includeCoreStrats && data.coreStratagems) {
    allStrats.push({ header: 'CORE STRATAGEMS', strats: data.coreStratagems });
  }
  if (options.includeDetachmentStrats && data.detachmentStratagems) {
    allStrats.push({ header: data.meta.detachment.toUpperCase(), strats: data.detachmentStratagems });
  }

  // Calculate card height to fill page
  const totalStrats = allStrats.reduce((sum, g) => sum + g.strats.length, 0);
  const headerSpace = allStrats.length * 20;
  const availableHeight = PAGE.height - PAGE.margin * 2 - headerSpace;
  const cardHeight = Math.min(42, Math.floor(availableHeight / totalStrats) - 3);

  for (const group of allStrats) {
    doc.font(FONT.bold).fontSize(14).fillColor(COLORS.headerBg);
    doc.text(group.header, PAGE.margin, y);
    y += 18;

    group.strats.forEach((strat, idx) => {
      renderStratagemCard(doc, strat, PAGE.margin, y, contentWidth, cardHeight, idx);
      y += cardHeight + 2;
    });
    y += 6;
  }
}

function renderReferencePage(doc, data, options) {
  const contentWidth = PAGE.width - PAGE.margin * 2;
  let y = PAGE.margin;

  // Keywords section (full width, stacked)
  if (options.includeKeywords && data.keywords) {
    doc.font(FONT.bold).fontSize(14).fillColor(COLORS.headerBg);
    doc.text('KEYWORD REFERENCE', PAGE.margin, y);
    y += 20;

    // Two-column layout for keywords
    const keywords = Object.entries(data.keywords);
    const colWidth = (contentWidth - 20) / 2;
    const midpoint = Math.ceil(keywords.length / 2);

    const leftStartY = y;
    let leftY = y;
    let rightY = y;

    for (let i = 0; i < keywords.length; i++) {
      const [key, desc] = keywords[i];
      const isLeft = i < midpoint;
      const currentX = isLeft ? PAGE.margin : PAGE.margin + colWidth + 20;
      const currentY = isLeft ? leftY : rightY;

      doc.font(FONT.bold).fontSize(9).fillColor(COLORS.sectionHeader);
      doc.text(key, currentX, currentY);
      doc.font(FONT.regular).fontSize(8).fillColor(COLORS.text);
      doc.text(desc, currentX, currentY + 11, { width: colWidth });
      const h = doc.heightOfString(desc, { width: colWidth }) + 16;

      if (isLeft) leftY += h;
      else rightY += h;
    }
    y = Math.max(leftY, rightY) + 10;
  }

  // Points Summary (full width)
  if (options.includePoints && data.pointsSummary) {
    doc.font(FONT.bold).fontSize(14).fillColor(COLORS.headerBg);
    doc.text('POINTS SUMMARY', PAGE.margin, y);
    y += 20;

    // Table header
    doc.rect(PAGE.margin, y, contentWidth, 18).fill(COLORS.statsBg);
    doc.font(FONT.bold).fontSize(9).fillColor(COLORS.sectionHeader);
    doc.text('Unit', PAGE.margin + 8, y + 4);
    doc.text('Qty', PAGE.width - 140, y + 4, { width: 35, align: 'center' });
    doc.text('Each', PAGE.width - 100, y + 4, { width: 35, align: 'center' });
    doc.text('Total', PAGE.width - 55, y + 4, { width: 35, align: 'right' });
    y += 20;

    let totalPts = 0;
    doc.font(FONT.regular).fontSize(9).fillColor(COLORS.text);

    for (const item of data.pointsSummary) {
      const lineTotal = item.pts * item.qty;
      totalPts += lineTotal;
      doc.text(item.unit, PAGE.margin + 8, y);
      doc.text(String(item.qty), PAGE.width - 140, y, { width: 35, align: 'center' });
      doc.text(String(item.pts), PAGE.width - 100, y, { width: 35, align: 'center' });
      doc.text(String(lineTotal), PAGE.width - 55, y, { width: 35, align: 'right' });
      y += 14;
    }

    y += 2;
    doc.rect(PAGE.margin, y, contentWidth, 1).fill(COLORS.border);
    y += 8;

    doc.font(FONT.bold).fontSize(11).fillColor(COLORS.headerBg);
    doc.text('TOTAL', PAGE.margin + 8, y);
    doc.text(`${totalPts} pts`, PAGE.width - 70, y, { width: 50, align: 'right' });
    y += 25;
  }

  // Faction & Detachment Rules at bottom
  if (data.factionRule || data.detachmentRule) {
    doc.rect(PAGE.margin, y, contentWidth, 2).fill(COLORS.headerBg);
    y += 10;

    if (data.factionRule) {
      doc.font(FONT.bold).fontSize(11).fillColor(COLORS.headerBg);
      doc.text(`FACTION RULE: ${data.factionRule.name}`, PAGE.margin, y);
      y += 14;
      doc.font(FONT.regular).fontSize(10).fillColor(COLORS.text);
      doc.text(data.factionRule.effect, PAGE.margin, y, { width: contentWidth });
      y += doc.heightOfString(data.factionRule.effect, { width: contentWidth }) + 12;
    }

    if (data.detachmentRule) {
      doc.font(FONT.bold).fontSize(11).fillColor(COLORS.headerBg);
      doc.text(`DETACHMENT RULE: ${data.detachmentRule.name}`, PAGE.margin, y);
      y += 14;
      doc.font(FONT.regular).fontSize(10).fillColor(COLORS.text);
      doc.text(data.detachmentRule.effect, PAGE.margin, y, { width: contentWidth });
    }
  }
}
