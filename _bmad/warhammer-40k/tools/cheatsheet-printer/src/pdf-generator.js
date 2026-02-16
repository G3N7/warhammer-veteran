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

// Black & White optimized colors for printing
const BW_COLORS = {
  headerBg: '#000000',      // Pure black
  headerText: '#ffffff',    // White
  statsBg: '#e0e0e0',       // Light gray, good contrast
  statsLabelBg: '#cccccc',  // Slightly darker
  sectionHeader: '#000000', // Black
  text: '#000000',          // Black
  lightText: '#333333',     // Dark gray
  border: '#000000',        // Black borders for clarity
  accent: '#000000',        // Black
  cpBg: '#000000',          // Black
  cpText: '#ffffff',        // White
  // Stratagem alternating backgrounds
  stratagemOdd: '#ffffff',
  stratagemEven: '#f0f0f0'
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

    // Select color scheme based on B&W mode
    const colors = options.bwMode ? BW_COLORS : COLORS;
    const strokeWidth = options.bwMode ? 1.5 : 1; // Thicker borders in B&W mode

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
          renderUnitCard(doc, unit, x, y, colors, strokeWidth);
        });
      }
    }

    // Phase Reminders page (quick turn reference - right after datasheets)
    if (options.includePhaseReminders && data.phaseReminders) {
      doc.addPage();
      renderPhaseRemindersPage(doc, data, colors, strokeWidth);
    }

    // Stratagems page (stacked vertically, bigger text)
    if ((options.includeCoreStrats && data.coreStratagems) || (options.includeDetachmentStrats && data.detachmentStratagems)) {
      doc.addPage();
      renderStratagemsPage(doc, data, options, colors, strokeWidth);
    }

    // Reference page: Keywords, Points, then Faction/Detachment rules
    if ((options.includeKeywords && data.keywords) || (options.includePoints && data.pointsSummary)) {
      doc.addPage();
      renderReferencePage(doc, data, options, colors);
    }

    doc.end();

    stream.on('finish', resolve);
    stream.on('error', reject);
  });
}

// No longer expanding units - each unit type appears once with qty indicator

// No title page - jump straight to content

function renderUnitCard(doc, unit, x, y, colors = COLORS, strokeWidth = 1) {
  const padding = 2;
  const innerWidth = CARD.width - padding * 2;
  const qty = unit.qty || 1;

  // Card border
  doc.lineWidth(strokeWidth).rect(x, y, CARD.width, CARD.height).stroke(colors.border);

  // Header bar with unit name and points
  doc.rect(x, y, CARD.width, 14).fill(colors.headerBg);
  doc.font(FONT.bold).fontSize(10).fillColor(colors.headerText);
  const nameText = qty > 1 ? `${unit.name.toUpperCase()} x${qty}` : unit.name.toUpperCase();
  doc.text(nameText, x + padding + 1, y + 2, { width: innerWidth - 35, lineBreak: false });
  doc.text(`${unit.pts}`, x + CARD.width - 32, y + 2, { width: 30, align: 'right', lineBreak: false });

  let currentY = y + 15;

  // Stats bar - large and prominent
  const stats = unit.stats;
  const statWidth = innerWidth / 8;
  const statsHeight = 22;

  doc.rect(x + padding, currentY, innerWidth, statsHeight).fill(colors.statsBg);

  const statLabels = ['M', 'T', 'SV', 'W', 'LD', 'OC', 'INV', 'FNP'];
  const statValues = [
    stats.M || '-', stats.T || '-', stats.SV || '-', stats.W || '-',
    stats.LD || '-', stats.OC ?? '-', stats.INV || '-', stats.FNP || '-'
  ];

  statLabels.forEach((label, i) => {
    const sx = x + padding + i * statWidth;
    doc.font(FONT.bold).fontSize(7).fillColor(colors.lightText);
    doc.text(label, sx, currentY + 1, { width: statWidth, align: 'center', lineBreak: false });
    doc.font(FONT.bold).fontSize(12).fillColor(colors.text);
    doc.text(String(statValues[i]), sx, currentY + 9, { width: statWidth, align: 'center', lineBreak: false });
  });

  currentY += statsHeight + 1;

  // Calculate space for content - footer gets 2 lines for wrapping
  const footerHeight = 20;
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
    doc.font(FONT.bold).fontSize(fontSize).fillColor(colors.text);
    doc.text(`${wpn.name}: `, x + padding, currentY, { continued: true, lineBreak: false });
    doc.font(FONT.regular).fontSize(fontSize).fillColor(colors.text);
    // Filter out redundant tags (e.g., "Pistol" when weapon name contains "Pistol")
    const filteredTags = wpn.tags.filter(tag => {
      if (tag.toLowerCase() === 'pistol' && wpn.name.toLowerCase().includes('pistol')) return false;
      return true;
    });
    const profileText = filteredTags.length > 0 ? `${wpn.profile} [${filteredTags.join(',')}]` : wpn.profile;
    doc.text(profileText, { lineBreak: false });
    currentY += lineHeight;
  }

  // Abilities
  for (const ability of unit.abilities) {
    if (currentY + lineHeight > contentEnd) break;
    doc.font(FONT.regular).fontSize(fontSize).fillColor(colors.text);
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
    footerParts.push(`Leads: ${unit.leads.join(', ')}`);
  }

  // Add notes
  if (unit.notes) footerParts.push(unit.notes);

  if (footerParts.length > 0) {
    const footerText = footerParts.join(' | ');
    doc.font(FONT.bold).fontSize(7).fillColor(colors.accent);
    // Allow wrapping within footer area, clip to available height
    doc.text(footerText, x + padding, bottomY, { width: innerWidth, height: footerHeight, ellipsis: true });
  }
}

function renderStratagemCard(doc, strat, x, y, width, height, index = 0, colors = COLORS, strokeWidth = 1) {
  const padding = 5;
  const innerWidth = width - padding * 2;

  // Card background (alternating)
  const bgColor = index % 2 === 0 ? colors.stratagemOdd : colors.stratagemEven;
  doc.lineWidth(strokeWidth).rect(x, y, width, height).fill(bgColor).stroke(colors.border);

  // CP badge on left
  doc.font(FONT.bold).fontSize(10).fillColor(colors.cpBg);
  doc.text(`${strat.cp}CP`, x + padding, y + 4, { width: 28 });

  // Stratagem name
  doc.font(FONT.bold).fontSize(10).fillColor(colors.headerBg);
  doc.text(strat.name.toUpperCase(), x + 38, y + 4, { width: innerWidth - 38 });

  // Phase on same line, right-aligned
  const phaseText = strat.type ? `${strat.phase} | ${strat.type}` : strat.phase;
  doc.font(FONT.regular).fontSize(7).fillColor(colors.accent);
  doc.text(phaseText, x + width - 100, y + 6, { width: 95, align: 'right' });

  // Effect - bigger font
  doc.font(FONT.regular).fontSize(9).fillColor(colors.text);
  doc.text(strat.effect, x + padding, y + 18, { width: innerWidth, height: height - 22 });
}

function renderStratagemsPage(doc, data, options, colors = COLORS, strokeWidth = 1) {
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
    doc.font(FONT.bold).fontSize(14).fillColor(colors.headerBg);
    doc.text(group.header, PAGE.margin, y);
    y += 18;

    group.strats.forEach((strat, idx) => {
      renderStratagemCard(doc, strat, PAGE.margin, y, contentWidth, cardHeight, idx, colors, strokeWidth);
      y += cardHeight + 2;
    });
    y += 6;
  }
}

// Phase-specific colors for visual distinction
const PHASE_COLORS = {
  command:   { bg: '#1a365d', text: '#ffffff' },  // Navy blue
  movement:  { bg: '#276749', text: '#ffffff' },  // Forest green
  shooting:  { bg: '#9b2c2c', text: '#ffffff' },  // Crimson
  charge:    { bg: '#c05621', text: '#ffffff' },  // Orange
  fight:     { bg: '#553c9a', text: '#ffffff' },  // Purple
  endOfTurn: { bg: '#4a5568', text: '#ffffff' }   // Slate gray
};

const PHASE_COLORS_BW = {
  command:   { bg: '#000000', text: '#ffffff' },
  movement:  { bg: '#333333', text: '#ffffff' },
  shooting:  { bg: '#000000', text: '#ffffff' },
  charge:    { bg: '#333333', text: '#ffffff' },
  fight:     { bg: '#000000', text: '#ffffff' },
  endOfTurn: { bg: '#333333', text: '#ffffff' }
};

function renderPhaseRemindersPage(doc, data, colors = COLORS, strokeWidth = 1) {
  const contentWidth = PAGE.width - PAGE.margin * 2;
  const isBW = colors === BW_COLORS;
  const phaseColors = isBW ? PHASE_COLORS_BW : PHASE_COLORS;

  const phases = [
    { key: 'command', label: 'COMMAND' },
    { key: 'movement', label: 'MOVEMENT' },
    { key: 'shooting', label: 'SHOOTING' },
    { key: 'charge', label: 'CHARGE' },
    { key: 'fight', label: 'FIGHT' },
    { key: 'endOfTurn', label: 'END OF TURN' }
  ];

  // Collect active phases
  const activePhases = phases.filter(p => {
    const r = data.phaseReminders[p.key];
    return r && r.length > 0;
  });

  // Auto-scale: measure total height at default size, shrink if needed to fit one page
  const availableHeight = PAGE.height - PAGE.margin * 2;
  const headerHeight = 18;
  const phaseGap = 6;
  const itemPad = 3;
  let textFontSize = 11;
  const minFontSize = 7;

  // Measure total height at a given font size
  function measureTotal(fontSize) {
    let total = 0;
    for (const phase of activePhases) {
      const reminders = data.phaseReminders[phase.key];
      total += headerHeight + 3; // header + gap after header
      for (const reminder of reminders) {
        const text = typeof reminder === 'string' ? reminder : reminder.text;
        const priority = typeof reminder === 'object' ? reminder.priority : 2;
        const font = priority === 1 ? FONT.bold : FONT.regular;
        doc.font(font).fontSize(fontSize);
        const h = doc.heightOfString(`• ${text}`, { width: contentWidth - 16 });
        total += h + itemPad;
      }
      total += phaseGap;
    }
    return total;
  }

  // Shrink font until content fits on one page
  while (textFontSize > minFontSize && measureTotal(textFontSize) > availableHeight) {
    textFontSize -= 0.5;
  }

  const headerFontSize = Math.min(13, textFontSize + 2);
  let y = PAGE.margin;

  // Render phases
  for (const phase of activePhases) {
    const reminders = data.phaseReminders[phase.key];
    const pColor = phaseColors[phase.key] || phaseColors.command;

    // Page break if needed
    if (y + headerHeight + 20 > PAGE.height - PAGE.margin) {
      doc.addPage();
      y = PAGE.margin;
    }

    // Phase header bar
    doc.rect(PAGE.margin, y, contentWidth, headerHeight).fill(pColor.bg);
    doc.font(FONT.bold).fontSize(headerFontSize).fillColor(pColor.text);
    doc.text(phase.label, PAGE.margin + 6, y + 3);
    y += headerHeight + 3;

    // Reminder items
    for (const reminder of reminders) {
      const text = typeof reminder === 'string' ? reminder : reminder.text;
      const priority = typeof reminder === 'object' ? reminder.priority : 2;

      if (priority === 1) {
        doc.font(FONT.bold).fontSize(textFontSize).fillColor(colors.text);
      } else if (priority === 3) {
        doc.font(FONT.regular).fontSize(textFontSize).fillColor(colors.lightText);
      } else {
        doc.font(FONT.regular).fontSize(textFontSize).fillColor(colors.text);
      }

      // Measure actual text height before rendering
      const textHeight = doc.heightOfString(`• ${text}`, { width: contentWidth - 16 });

      // Page break if this item won't fit
      if (y + textHeight > PAGE.height - PAGE.margin) {
        doc.addPage();
        y = PAGE.margin;
      }

      doc.text(`• ${text}`, PAGE.margin + 8, y, { width: contentWidth - 16 });
      y += textHeight + itemPad;
    }

    y += phaseGap;
  }
}

function renderReferencePage(doc, data, options, colors = COLORS) {
  const contentWidth = PAGE.width - PAGE.margin * 2;
  let y = PAGE.margin;

  // Keywords section (full width, stacked)
  if (options.includeKeywords && data.keywords) {
    doc.font(FONT.bold).fontSize(14).fillColor(colors.headerBg);
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

      doc.font(FONT.bold).fontSize(9).fillColor(colors.sectionHeader);
      doc.text(key, currentX, currentY);
      doc.font(FONT.regular).fontSize(8).fillColor(colors.text);
      doc.text(desc, currentX, currentY + 11, { width: colWidth });
      const h = doc.heightOfString(desc, { width: colWidth }) + 16;

      if (isLeft) leftY += h;
      else rightY += h;
    }
    y = Math.max(leftY, rightY) + 10;
  }

  // Points Summary (full width)
  if (options.includePoints && data.pointsSummary) {
    doc.font(FONT.bold).fontSize(14).fillColor(colors.headerBg);
    doc.text('POINTS SUMMARY', PAGE.margin, y);
    y += 20;

    // Table header
    doc.rect(PAGE.margin, y, contentWidth, 18).fill(colors.statsBg);
    doc.font(FONT.bold).fontSize(9).fillColor(colors.sectionHeader);
    doc.text('Unit', PAGE.margin + 8, y + 4);
    doc.text('Qty', PAGE.width - 140, y + 4, { width: 35, align: 'center' });
    doc.text('Each', PAGE.width - 100, y + 4, { width: 35, align: 'center' });
    doc.text('Total', PAGE.width - 55, y + 4, { width: 35, align: 'right' });
    y += 20;

    let totalPts = 0;
    doc.font(FONT.regular).fontSize(9).fillColor(colors.text);

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
    doc.rect(PAGE.margin, y, contentWidth, 1).fill(colors.border);
    y += 8;

    doc.font(FONT.bold).fontSize(11).fillColor(colors.headerBg);
    doc.text('TOTAL', PAGE.margin + 8, y);
    doc.text(`${totalPts} pts`, PAGE.width - 70, y, { width: 50, align: 'right' });
    y += 25;
  }

  // Faction & Detachment Rules at bottom
  if (data.factionRule || data.detachmentRule) {
    doc.rect(PAGE.margin, y, contentWidth, 2).fill(colors.headerBg);
    y += 10;

    if (data.factionRule) {
      doc.font(FONT.bold).fontSize(11).fillColor(colors.headerBg);
      doc.text(`FACTION RULE: ${data.factionRule.name}`, PAGE.margin, y);
      y += 14;
      doc.font(FONT.regular).fontSize(10).fillColor(colors.text);
      doc.text(data.factionRule.effect, PAGE.margin, y, { width: contentWidth });
      y += doc.heightOfString(data.factionRule.effect, { width: contentWidth }) + 12;
    }

    if (data.detachmentRule) {
      doc.font(FONT.bold).fontSize(11).fillColor(colors.headerBg);
      doc.text(`DETACHMENT RULE: ${data.detachmentRule.name}`, PAGE.margin, y);
      y += 14;
      doc.font(FONT.regular).fontSize(10).fillColor(colors.text);
      doc.text(data.detachmentRule.effect, PAGE.margin, y, { width: contentWidth });
    }
  }
}
