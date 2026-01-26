#!/usr/bin/env node

import { program } from 'commander';
import { generatePDF } from './pdf-generator.js';
import { readFileSync } from 'fs';
import { resolve } from 'path';

program
  .name('wh40k-print')
  .description('Generate compact printable datasheets for Warhammer 40K army lists')
  .version('1.0.0')
  .argument('<cheatsheet>', 'Path to .cheatsheet.json file')
  .option('-o, --output <path>', 'Output PDF path (default: same name as input with .pdf)')
  .option('--no-datasheets', 'Omit unit datasheet cards')
  .option('--no-keywords', 'Omit keyword glossary')
  .option('--no-points', 'Omit points summary')
  .option('--no-core-strats', 'Omit core stratagems page')
  .option('--no-detachment-strats', 'Omit detachment stratagems page')
  .option('--only-datasheets', 'Only print datasheets (no reference pages)')
  .option('--only-reference', 'Only print reference pages (no datasheets)')
  .option('--no-phase-reminders', 'Omit phase reminders page')
  .option('--bw', 'Optimize for black & white printing')
  .action(async (cheatsheetPath, options) => {
    try {
      const fullPath = resolve(cheatsheetPath);
      const data = JSON.parse(readFileSync(fullPath, 'utf-8'));

      const outputPath = options.output || fullPath.replace('.cheatsheet.json', '-cheatsheet.pdf');

      // Handle convenience flags
      let includeDatasheets = options.datasheets !== false;
      let includeKeywords = options.keywords !== false;
      let includePoints = options.points !== false;
      let includeCoreStrats = options.coreStrats !== false;
      let includeDetachmentStrats = options.detachmentStrats !== false;
      let includePhaseReminders = options.phaseReminders !== false;

      if (options.onlyDatasheets) {
        includeKeywords = false;
        includePoints = false;
        includeCoreStrats = false;
        includeDetachmentStrats = false;
        includePhaseReminders = false;
      }

      if (options.onlyReference) {
        includeDatasheets = false;
      }

      console.log(`Generating cheatsheet PDF for: ${data.meta.name}`);
      console.log(`  Faction: ${data.meta.faction}`);
      console.log(`  Detachment: ${data.meta.detachment}`);
      console.log(`  Points: ${data.meta.points}/${data.meta.battleSize}`);
      console.log(`  Units: ${data.units.length}`);
      if (options.bw) {
        console.log(`  Mode: Black & White (print optimized)`);
      }
      console.log('');
      console.log('Sections:');
      console.log(`  [${includeDatasheets ? 'x' : ' '}] Datasheets`);
      console.log(`  [${includePhaseReminders ? 'x' : ' '}] Phase Reminders`);
      console.log(`  [${includeCoreStrats ? 'x' : ' '}] Core Stratagems`);
      console.log(`  [${includeDetachmentStrats ? 'x' : ' '}] Detachment Stratagems`);
      console.log(`  [${includeKeywords ? 'x' : ' '}] Keywords`);
      console.log(`  [${includePoints ? 'x' : ' '}] Points Summary`);
      console.log('');

      await generatePDF(data, outputPath, {
        includeDatasheets,
        includeKeywords,
        includePoints,
        includeCoreStrats,
        includeDetachmentStrats,
        includePhaseReminders,
        bwMode: options.bw
      });

      console.log(`PDF generated: ${outputPath}`);
    } catch (err) {
      console.error('Error:', err.message);
      process.exit(1);
    }
  });

program.parse();
