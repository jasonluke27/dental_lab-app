"""Add created_date and updated_date to Job

Revision ID: 82833fb436c9
Revises: c23dc23c9b32
Create Date: 2024-07-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '82833fb436c9'
down_revision = 'c23dc23c9b32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'job_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_type', sa.String(length=64), nullable=True),
        sa.Column('practice_name', sa.String(length=64), nullable=True),
        sa.Column('doctor_name', sa.String(length=64), nullable=True),
        sa.Column('patient_name', sa.String(length=64), nullable=True),
        sa.Column('lab_slip_number', sa.String(length=64), nullable=True),
        sa.Column('job_status', sa.String(length=64), nullable=True),
        sa.Column('due_date', sa.Date, nullable=True),
        sa.Column('shade', sa.String(length=64), nullable=True),
        sa.Column('invoice_number', sa.String(length=64), nullable=True),
        sa.Column('delivery_info', sa.String(length=64), nullable=True),
        sa.Column('comments', sa.Text, nullable=True),
        sa.Column('created_date', sa.DateTime, nullable=True),
        sa.Column('updated_date', sa.DateTime, nullable=True),
    )
    
    # Copy data from old table to new table
    job_table = table('job',
                      column('id', Integer),
                      column('job_type', String),
                      column('practice_name', String),
                      column('doctor_name', String),
                      column('patient_name', String),
                      column('lab_slip_number', String),
                      column('job_status', String),
                      column('due_date', sa.Date),
                      column('shade', String),
                      column('invoice_number', String),
                      column('delivery_info', String),
                      column('comments', sa.Text),
                      )

    job_new_table = table('job_new',
                          column('id', Integer),
                          column('job_type', String),
                          column('practice_name', String),
                          column('doctor_name', String),
                          column('patient_name', String),
                          column('lab_slip_number', String),
                          column('job_status', String),
                          column('due_date', sa.Date),
                          column('shade', String),
                          column('invoice_number', String),
                          column('delivery_info', String),
                          column('comments', sa.Text),
                          )

    connection = op.get_bind()
    for row in connection.execute(job_table.select()):
        connection.execute(job_new_table.insert().values(
            id=row.id,
            job_type=row.job_type,
            practice_name=row.practice_name,
            doctor_name=row.doctor_name,
            patient_name=row.patient_name,
            lab_slip_number=row.lab_slip_number,
            job_status=row.job_status,
            due_date=row.due_date,
            shade=row.shade,
            invoice_number=row.invoice_number,
            delivery_info=row.delivery_info,
            comments=row.comments,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        ))

    # Drop the old table
    op.drop_table('job')

    # Rename the new table to the old table name
    op.rename_table('job_new', 'job')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'job_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_type', sa.String(length=64), nullable=True),
        sa.Column('practice_name', sa.String(length=64), nullable=True),
        sa.Column('doctor_name', sa.String(length=64), nullable=True),
        sa.Column('patient_name', sa.String(length=64), nullable=True),
        sa.Column('lab_slip_number', sa.String(length=64), nullable=True),
        sa.Column('job_status', sa.String(length=64), nullable=True),
        sa.Column('due_date', sa.Date, nullable=True),
        sa.Column('shade', sa.String(length=64), nullable=True),
        sa.Column('invoice_number', sa.String(length=64), nullable=True),
        sa.Column('delivery_info', sa.String(length=64), nullable=True),
        sa.Column('comments', sa.Text, nullable=True),
    )

    # Copy data from new table to old table
    job_table = table('job_new',
                      column('id', Integer),
                      column('job_type', String),
                      column('practice_name', String),
                      column('doctor_name', String),
                      column('patient_name', String),
                      column('lab_slip_number', String),
                      column('job_status', String),
                      column('due_date', sa.Date),
                      column('shade', String),
                      column('invoice_number', String),
                      column('delivery_info', String),
                      column('comments', sa.Text),
                      )

    job_old_table = table('job_old',
                          column('id', Integer),
                          column('job_type', String),
                          column('practice_name', String),
                          column('doctor_name', String),
                          column('patient_name', String),
                          column('lab_slip_number', String),
                          column('job_status', String),
                          column('due_date', sa.Date),
                          column('shade', String),
                          column('invoice_number', String),
                          column('delivery_info', String),
                          column('comments', sa.Text),
                          )

    connection = op.get_bind()
    for row in connection.execute(job_table.select()):
        connection.execute(job_old_table.insert().values(
            id=row.id,
            job_type=row.job_type,
            practice_name=row.practice_name,
            doctor_name=row.doctor_name,
            patient_name=row.patient_name,
            lab_slip_number=row.lab_slip_number,
            job_status=row.job_status,
            due_date=row.due_date,
            shade=row.shade,
            invoice_number=row.invoice_number,
            delivery_info=row.delivery_info,
            comments=row.comments,
        ))

    # Drop the new table
    op.drop_table('job_new')

    # Rename the old table to the old table name
    op.rename_table('job_old', 'job')
    # ### end Alembic commands ###
