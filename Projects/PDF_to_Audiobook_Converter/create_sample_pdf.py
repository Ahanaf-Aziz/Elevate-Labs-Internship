"""
Create sample PDF files for testing the converter.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch


def create_sample_pdf():
    """Create a sample PDF with text content."""
    
    # Sample text content
    sample_text = """
    <b>The Future of Technology</b>
    
    <p>Technology has become an integral part of our daily lives. From smartphones to artificial intelligence, 
    innovations continue to shape how we work, communicate, and live.</p>
    
    <p><b>Artificial Intelligence</b></p>
    <p>Artificial Intelligence is revolutionizing industries across the globe. Machine learning algorithms 
    can now recognize patterns, make predictions, and automate complex tasks that once required human expertise.</p>
    
    <p><b>Cloud Computing</b></p>
    <p>Cloud computing has transformed how businesses store and process data. Companies can now scale their 
    infrastructure on demand, reducing costs and improving efficiency.</p>
    
    <p><b>Cybersecurity</b></p>
    <p>As technology advances, so do the threats. Cybersecurity has become more important than ever, with 
    organizations investing heavily in protecting their digital assets.</p>
    
    <p><b>The Internet of Things</b></p>
    <p>The Internet of Things connects billions of devices worldwide. Smart homes, wearable devices, and 
    connected vehicles are just the beginning of this technological revolution.</p>
    
    <p>The future promises even more exciting developments. As we continue to innovate and push the boundaries 
    of what's possible, technology will undoubtedly play a central role in shaping our world.</p>
    """
    
    # Create PDF
    doc = SimpleDocTemplate("sample_technology.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add content
    for line in sample_text.strip().split('\n'):
        if line.strip():
            p = Paragraph(line.strip(), styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 0.2*inch))
    
    doc.build(story)
    print("Created: sample_technology.pdf")


def create_sample_pdf_2():
    """Create another sample PDF."""
    
    sample_text = """
    <b>Introduction to Python Programming</b>
    
    <p>Python is a versatile and beginner-friendly programming language that has gained immense popularity 
    in recent years. Its simple syntax and powerful libraries make it ideal for various applications.</p>
    
    <p><b>Why Learn Python?</b></p>
    <p>Python is used in web development, data science, artificial intelligence, automation, and many other fields. 
    Learning Python opens doors to numerous career opportunities.</p>
    
    <p><b>Getting Started</b></p>
    <p>To start programming in Python, you need to install the Python interpreter and a text editor or IDE. 
    Popular choices include Visual Studio Code, PyCharm, and Jupyter Notebook.</p>
    
    <p><b>Basic Concepts</b></p>
    <p>Understanding variables, data types, loops, and functions is essential for any programmer. 
    These fundamental concepts form the building blocks of all programs.</p>
    
    <p><b>Libraries and Frameworks</b></p>
    <p>Python has a rich ecosystem of libraries and frameworks. NumPy for numerical computing, Django for web development, 
    and TensorFlow for machine learning are just a few examples.</p>
    
    <p>With dedication and practice, anyone can become proficient in Python programming and build amazing applications.</p>
    """
    
    doc = SimpleDocTemplate("sample_python.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    for line in sample_text.strip().split('\n'):
        if line.strip():
            p = Paragraph(line.strip(), styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 0.2*inch))
    
    doc.build(story)
    print("Created: sample_python.pdf")


if __name__ == "__main__":
    try:
        create_sample_pdf()
        create_sample_pdf_2()
        print("\nSample PDFs created successfully!")
    except ImportError:
        print("Error: reportlab is required to create sample PDFs")
        print("Install it with: pip install reportlab")
