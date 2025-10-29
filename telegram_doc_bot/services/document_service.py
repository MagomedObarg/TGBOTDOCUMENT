"""
Сервис для создания документов Word и PDF.
Форматирует и сохраняет сгенерированный текст в различные форматы.
"""

import logging
import os
from datetime import datetime
from typing import Optional
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

logger = logging.getLogger(__name__)


class DocumentService:
    """Класс для создания документов в различных форматах"""
    
    def __init__(self, output_dir: str = 'generated_docs'):
        """
        Инициализация сервиса генерации документов
        
        Args:
            output_dir: Директория для сохранения документов
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Document сервис инициализирован, директория: {output_dir}")
    
    async def create_word_document(
        self,
        content: str,
        title: str = "Документ",
        user_id: int = 0
    ) -> Optional[str]:
        """
        Создание документа Word (.docx)
        
        Args:
            content: Текстовое содержимое документа
            title: Заголовок документа
            user_id: ID пользователя для имени файла
        
        Returns:
            Путь к созданному файлу или None в случае ошибки
        """
        try:
            # Создание нового документа
            doc = Document()
            
            # Настройка параметров документа
            sections = doc.sections
            for section in sections:
                section.top_margin = Inches(1)
                section.bottom_margin = Inches(1)
                section.left_margin = Inches(1)
                section.right_margin = Inches(1)
            
            # Добавление заголовка
            heading = doc.add_heading(title, level=1)
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Добавление даты
            date_paragraph = doc.add_paragraph()
            date_run = date_paragraph.add_run(
                f"Дата создания: {datetime.now().strftime('%d.%m.%Y')}"
            )
            date_run.font.size = Pt(10)
            date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            doc.add_paragraph()  # Пустая строка
            
            # Разбивка контента на параграфы и добавление в документ
            paragraphs = content.split('\n\n')
            for para_text in paragraphs:
                if para_text.strip():
                    # Проверка на заголовок (если строка короткая и заканчивается двоеточием или полностью заглавная)
                    if len(para_text) < 100 and (para_text.strip().endswith(':') or para_text.strip().isupper()):
                        para = doc.add_heading(para_text.strip(), level=2)
                    else:
                        para = doc.add_paragraph(para_text.strip())
                        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                        
                        # Форматирование текста
                        for run in para.runs:
                            run.font.name = 'Times New Roman'
                            run.font.size = Pt(12)
            
            # Генерация имени файла
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"document_{user_id}_{timestamp}.docx"
            filepath = os.path.join(self.output_dir, filename)
            
            # Сохранение документа
            doc.save(filepath)
            logger.info(f"Word документ создан: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Ошибка при создании Word документа: {e}")
            return None
    
    async def create_pdf_document(
        self,
        content: str,
        title: str = "Документ",
        user_id: int = 0
    ) -> Optional[str]:
        """
        Создание PDF документа
        
        Args:
            content: Текстовое содержимое документа
            title: Заголовок документа
            user_id: ID пользователя для имени файла
        
        Returns:
            Путь к созданному файлу или None в случае ошибки
        """
        try:
            # Генерация имени файла
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"document_{user_id}_{timestamp}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Создание PDF документа
            doc = SimpleDocTemplate(filepath, pagesize=A4,
                                   rightMargin=inch, leftMargin=inch,
                                   topMargin=inch, bottomMargin=inch)
            
            # Контейнер для элементов документа
            story = []
            
            # Стили
            styles = getSampleStyleSheet()
            
            # Стиль для заголовка
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor='black',
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Times-Bold'
            )
            
            # Стиль для основного текста
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=12,
                leading=14,
                alignment=TA_JUSTIFY,
                fontName='Times-Roman'
            )
            
            # Стиль для подзаголовков
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor='black',
                spaceAfter=12,
                fontName='Times-Bold'
            )
            
            # Добавление заголовка
            story.append(Paragraph(title, title_style))
            
            # Добавление даты
            date_text = f"Дата создания: {datetime.now().strftime('%d.%m.%Y')}"
            story.append(Paragraph(date_text, body_style))
            story.append(Spacer(1, 0.3 * inch))
            
            # Разбивка контента на параграфы
            paragraphs = content.split('\n\n')
            for para_text in paragraphs:
                if para_text.strip():
                    # Экранирование специальных символов для ReportLab
                    para_text = para_text.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    
                    # Проверка на заголовок
                    if len(para_text) < 100 and (para_text.endswith(':') or para_text.isupper()):
                        story.append(Paragraph(para_text, heading_style))
                    else:
                        story.append(Paragraph(para_text, body_style))
                    
                    story.append(Spacer(1, 0.2 * inch))
            
            # Сборка документа
            doc.build(story)
            logger.info(f"PDF документ создан: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Ошибка при создании PDF документа: {e}")
            return None
    
    def cleanup_file(self, filepath: str) -> bool:
        """
        Удаление временного файла
        
        Args:
            filepath: Путь к файлу для удаления
        
        Returns:
            True если файл удалён успешно, False в противном случае
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Файл удалён: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при удалении файла {filepath}: {e}")
            return False
